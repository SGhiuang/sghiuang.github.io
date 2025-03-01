# main.py
from js import document

def show_menu():
    """激活主菜单界面"""
    document.getElementById("menu").style.display = "block"
    document.getElementById("experiment1").classList.remove("active")
    document.getElementById("experiment2").classList.remove("active")

def select_experiment(num):
    """处理实验选择（由JavaScript调用）"""
    if num == 1:
        document.getElementById("experiment1").classList.add("active")
        document.getElementById("experiment2").classList.remove("active")
    elif num == 2:
        document.getElementById("experiment2").classList.add("active")
        document.getElementById("experiment1").classList.remove("active")

def exit_system():
    """清理资源"""
    document.getElementById("output1").innerHTML = ""
    document.getElementById("output2").innerHTML = ""
    show_menu()

if __name__ == "__main__":
    # Pyodide加载后自动执行
    show_menu()