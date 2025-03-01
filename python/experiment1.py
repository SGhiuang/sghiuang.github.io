# experiment1.py
import numpy as np
from js import document, console

def web_print(msg, target="output1"):
    """输出到指定DOM元素"""
    output = document.getElementById(target)
    output.innerHTML += f"<div>{msg}</div>"
    output.scrollTop = output.scrollHeight  # 自动滚动到底部

def parse_input(input_str, dtype=float):
    """解析网页输入数据"""
    try:
        return [dtype(x.strip()) for x in input_str.split(",") if x.strip()]
    except Exception as e:
        web_print(f"输入解析错误: {str(e)}", "output1")
        raise

def main(theta_str, u_str, m1, m2, experiments_data):
    """主处理函数（由JavaScript调用）"""
    try:
        # 清除旧输出
        document.getElementById("output1").innerHTML = ""
        
        # 数据预处理
        theta = np.array(parse_input(theta_str))
        u = np.array(parse_input(u_str))
        m1 = float(m1) / 1000  # 转换为kg
        m2 = float(m2) / 1000
        
        # 核心计算逻辑（保持原始算法不变）
        I = u  # I(μA) = u(mV)/R(kΩ)
        coefficients = np.polyfit(theta, I, 1)
        B, A = coefficients[0], coefficients[1]
        
        web_print("【传感器定标结果】")
        web_print(f"拟合方程: I = {B:.2f}θ + {A:.1f} (μA)")
        web_print(f"灵敏度 B = {B:.2f} μA/°C")

        # 实验数据处理
        results = []
        for data in experiments_data:
            m = float(data['m']) / 1000
            θ1 = float(data['θ1'])
            θ2 = float(data['θ2'])
            M = float(data['M']) / 1000
            
            # 原始计算逻辑
            Δθ = θ2 - θ1
            Q_absorb = (m*4187 + m1 * 900.2 + m2 * 900.2) * Δθ
            Q_release = M * 4187 * (100 - θ2)
            L = (Q_absorb - Q_release) / M
            
            # 结果存储
            results.append({
                'Δθ': Δθ,
                'L': L,
                'L_corr': L + 1796*Δθ/M  # 修正项
            })

        # 结果输出
        web_print("\n【实验计算结果】")
        for i, res in enumerate(results):
            web_print(f"第{i+1}组: Δθ={res['Δθ']:.2f}℃ | "
                     f"比汽化热={res['L']/1e6:.3f}×10⁶ J/kg | "
                     f"修正值={res['L_corr']/1e6:.3f}×10⁶ J/kg")

    except Exception as e:
        console.error(f"实验一错误: {str(e)}")
        web_print(f"<span style='color:red'>错误: {str(e)}</span>")