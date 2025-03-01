# main.py
from js import document, console

def show_menu():
    """安全显示主菜单"""
    try:
        menu = document.getElementById("menu")
        exp1 = document.getElementById("experiment1")
        exp2 = document.getElementById("experiment2")
        
        if not all([menu, exp1, exp2]):
            raise Exception("界面元素未正确初始化")
            
        menu.style.display = "block"
        exp1.style.display = "none"
        exp2.style.display = "none"
        console.log("主菜单已显示")
    except Exception as e:
        console.error(f"显示菜单时出错: {str(e)}")
        raise

def exit_system():
    """清理资源"""
    document.getElementById("menu").style.display = "none"
    document.getElementById("experiments").innerHTML = ""