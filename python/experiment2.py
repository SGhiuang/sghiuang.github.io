# experiment2.py
import numpy as np
from js import document, console

def web_print(msg, target="output2"):
    output = document.getElementById(target)
    output.innerHTML += f"<div>{msg}</div>"
    output.scrollTop = output.scrollHeight

def main(m_cu, t_cu_str, samples_data):
    """主处理函数（由JavaScript调用）"""
    try:
        document.getElementById("output2").innerHTML = ""
        
        # 数据处理
        t_cu = np.mean([float(x) for x in t_cu_str.split(",")])
        results = []
        
        # 核心计算逻辑
        for sample in samples_data:
            symbol = sample['symbol']
            M = float(sample['mass'])
            t = np.mean([float(x) for x in sample['times']])
            
            # 比热容计算
            C = 0.094 * (float(m_cu) * t_cu) / (M * t)
            
            # 标准值比对
            standard = {'Fe': 0.110, 'Al': 0.230}[symbol]
            error = abs(C - standard)/standard * 100
            
            results.append({
                'symbol': symbol,
                'C': C,
                'error': error
            })

        # 结果输出
        web_print("【实验结果对比】")
        web_print("金属 | 计算值 | 标准值 | 误差")
        web_print("-----------------------------")
        for res in results:
            web_print(f"{res['symbol']} | {res['C']:.3f} | "
                     f"{standard} | {res['error']:.1f}%")

    except Exception as e:
        console.error(f"实验二错误: {str(e)}")
        web_print(f"<span style='color:red'>错误: {str(e)}</span>")