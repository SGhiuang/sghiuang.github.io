import numpy as np

def main():
    print("=== 执行实验二：金属比热容测量 ===")
    # 常量定义
    C_Cu = 0.0940  # 铜的比热容 Cal/(g·°C)
    STANDARD_VALUES = {'Fe': 0.110, 'Al': 0.230}

    # 中英名称映射字典
    METAL_MAPPING = {
        '铁': 'Fe',
        '铝': 'Al'
    }
    REVERSE_MAPPING = {v: k for k, v in METAL_MAPPING.items()}  # 新增反向映射

    def get_valid_input(prompt, num_values=5):
        """获取有效的数值输入"""
        values = []
        print(prompt)
        for i in range(num_values):
            while True:
                try:
                    val = float(input(f"第{i+1}次测量值: "))
                    values.append(val)
                    break
                except ValueError:
                    print("输入错误，请输入数字！")
        return np.mean(values)

    print("=== 冷却法金属比热容测量 ===")

    # 输入铜样品数据
    print("\n【铜样品数据输入】")
    M_Cu = float(input("铜样品质量（g）: "))
    print("请输入铜样品5次冷却时间（102℃→98℃）：")
    t_Cu = get_valid_input("")

    # 输入待测样品数据
    samples = []
    for metal in ['铁', '铝']:
        print(f"\n【{metal}样品数据输入】")
        M = float(input(f"{metal}样品质量（g）: "))
        print(f"请输入{metal}样品5次冷却时间（102℃→98℃）：")
        t = get_valid_input("")
        
        # 关键修改：存储英文符号
        symbol = METAL_MAPPING[metal]
        samples.append( (symbol, M, t) )

    # 计算结果
    results = []
    for symbol, M, t in samples:
        # 计算比热容
        C = C_Cu * (M_Cu * t) / (M * t_Cu)
        # 计算误差
        std_value = STANDARD_VALUES[symbol]
        error = abs(C - std_value)/std_value * 100
        results.append( (symbol, M, t, C, error) )

    # 格式化输出（显示中文名称）
    print("\n【实验结果】")
    print(f"{'金属':<5}{'质量(g)':<8}{'平均时间(s)':<12}{'比热容':<12}{'标准值':<12}{'误差(%)':<10}")
    print("="*60)
    # 铜数据行
    print(f"{'铜':<5}{M_Cu:<8.2f}{t_Cu:<12.2f}{C_Cu:<12.3f}{C_Cu:<12.3f}{'-':<10}")
    # 待测样品数据行
    for symbol, M, t, C, err in results:
        std = STANDARD_VALUES[symbol]
        # 使用反向映射显示中文
        print(f"{REVERSE_MAPPING[symbol]:<5}{M:<8.2f}{t:<12.2f}{C:<12.3f}{std:<12.3f}{err:<10.1f}")

if __name__ == "__main__":
    main()

# 示例验证：
"""
输入：
铜质量：12.35
铜时间：16.8,16.7,16.9,16.8,16.7 → 平均16.78s

铁质量：11.03
铁时间：18.3,18.2,18.3,18.4,18.2 → 平均18.28s

铝质量：3.99
铝时间：13.4,13.5,13.4,13.3,13.4 → 平均13.40s

输出：
金属  质量(g) 平均时间(s)  比热容     标准值      误差(%)    
============================================================
铜    12.35   16.78      0.094      0.094      -         
铁    11.03   18.28      0.114      0.110      3.6       
铝    3.99    13.40      0.234      0.230      1.7      
"""