import experiment1
import experiment2

def show_menu():
    """显示选择菜单"""
    print("\n=== 物理实验数据处理系统 ===")
    print("1. 液体比汽化热测量实验")
    print("2. 金属比热容测量实验")
    print("3. 退出系统")

def run_experiment(choice):
    """执行对应的实验"""
    if choice == '1':
        experiment1.main()
    elif choice == '2':
        experiment2.main()
    else:
        print("无效的选择！")

def get_valid_selection():
    while True:
        try:
            selection = input("请选择实验编号 (1/2/3): ")
            if selection in ['1', '2', '3']:
                return selection
            raise ValueError
        except ValueError:
            print("输入错误，请输入1/2/3！")

if __name__ == "__main__":
    while True:
        selection = get_valid_selection()
        show_menu()
        selection = input("请选择实验编号 (1/2/3): ")
        
        if selection == '3':
            print("感谢使用，程序已退出！")
            break
            
        if selection in ['1', '2']:
            run_experiment(selection)
        else:
            print("输入错误，请重新输入1/2/3！")