import numpy as np

def main():
    print("=== 执行实验一：液体比汽化热测量 ===")
    # 常量定义
    Cw = 4187.0       # 水的比热容 J/(kg·°C)
    C_Al = 900.2      # 铝的比热容 J/(kg·°C)
    m3C3 = 1796.0     # 传感器热容量 J/K
    L_theory = 2.25e6 # 理论汽化热 J/kg

    def get_float_input(prompt):
        """获取有效的浮点数输入"""
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("输入错误，请输入有效的数字！")

    print("=== AD590传感器定标 ===")
    theta_input = input("请输入温度θ（摄氏度，以逗号分隔）: ").split(',')
    u_input = input("请输入对应电压u（mV，以逗号分隔）: ").split(',')

    theta = np.array(list(map(float, theta_input)))
    u = np.array(list(map(float, u_input)))
    I = u  # I(μA) = u(mV)/R(kΩ)，R=1000Ω时直接相等

    # 最小二乘法拟合
    coefficients = np.polyfit(theta, I, 1)
    B, A = coefficients[0], coefficients[1]

    print("\n【定标结果】")
    print(f"温度-电流关系式：I = {B:.2f}θ + {A:.1f} (μA)")
    print(f"传感器灵敏度 B = {B:.2f} μA/°C")

    print("\n=== 汽化热测量实验（输入3组数据） ===")

    # 输入固定参数（只需一次）
    print("\n▶ 固定参数输入（铝器质量）")
    m1 = get_float_input("铝量热器质量（g）: ") / 1000  # 转换为kg
    m2 = get_float_input("铝搅拌器质量（g）: ") / 1000  # 转换为kg

    experiments = []
    # 输入三组可变参数
    for i in range(3):
        print(f"\n▶▶ 第{i+1}组数据输入")
        m = get_float_input("量热器内水的质量（g）: ") / 1000
        θ1 = get_float_input("初始温度θ1（℃）: ")
        θ2 = get_float_input("最终温度θ2（℃）: ")
        M = get_float_input("凝结蒸汽质量（g）: ") / 1000
        
        experiments.append({
            'm': m, 'θ1': θ1, 'θ2': θ2, 'M': M
        })

    # 计算每组实验结果
    results = []
    for exp in experiments:
        # 提取参数（铝器质量使用固定值）
        m, θ1, θ2, M = exp['m'], exp['θ1'], exp['θ2'], exp['M']
        θ3 = 100.0  # 蒸汽温度
        Δθ = θ2 - θ1
        
        # 未修正计算
        Q_absorb = (m*Cw + m1*C_Al + m2*C_Al) * Δθ
        Q_release = M * Cw * (θ3 - θ2)
        L = (Q_absorb - Q_release) / M
        
        # 修正传感器影响
        Q_absorb_corr = Q_absorb + m3C3 * Δθ
        L_corr = (Q_absorb_corr - Q_release) / M

        # 计算偏差（带符号）
        deviation = (L - L_theory)/L_theory * 100
        deviation_corr = (L_corr - L_theory)/L_theory * 100
        
        results.append({
            'L': L, 
            'L_corr': L_corr,
            'Δθ': Δθ,
            'deviation': deviation,
            'deviation_corr': deviation_corr
        })

    # 计算平均结果
    avg_L = np.mean([x['L'] for x in results])
    avg_L_corr = np.mean([x['L_corr'] for x in results])

    # 结果输出
    print("\n【各组实验结果】")
    for i, res in enumerate(results):
        print(f"第{i+1}组: Δθ={res['Δθ']:.2f}℃ | "
            f"未修正L={res['L']/1e6:.3f}×10⁶ (偏差:{res['deviation']:+.1f}%) | "
            f"修正L'={res['L_corr']/1e6:.3f}×10⁶ (偏差:{res['deviation_corr']:+.1f}%)")

    # 计算最终平均偏差
    final_deviation = (avg_L - L_theory)/L_theory * 100
    final_deviation_corr = (avg_L_corr - L_theory)/L_theory * 100

    print("\n【最终结果】")
    print(f"铝器质量：量热器={m1 * 1000:.2f}g，搅拌器={m2 * 1000:.2f}g")
    print(f"平均比汽化热（未修正）: {avg_L/1e6:.3f}×10⁶ J/kg | 总偏差:{final_deviation:+.1f}%")
    print(f"平均比汽化热（修正后）: {avg_L_corr/1e6:.3f}×10⁶ J/kg | 总偏差:{final_deviation_corr:+.1f}%")

if __name__ == "__main__":
    main()

# 示例验证（输入以下数据测试）：
"""
传感器定标输入：
温度θ：13.90,19.25,24.90,29.80,32.50
电压u：285.7,291.1,296.8,301.8,304.5

固定参数：
铝量热器：46.45g
铝搅拌器：67.37g

三组实验数据：
第1组：水153.90g，θ1=12.92，θ2=37.03，蒸汽6.66g
第2组：水145.30g，θ1=13.05，θ2=36.50，蒸汽6.50g
第3组：水158.40g，θ1=12.85，θ2=37.20，蒸汽6.80g

预期输出：
修正后总偏差约-3.5%
"""