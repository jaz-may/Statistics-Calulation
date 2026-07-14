"""
    1.输入函数
        * 整数输入
        * 浮点数输入
        * 浮点数组输入
        * yes/no输入
        * 数据组输入
    2.数据处理
        * 求sample variance
"""
from typing import Callable, TypeVar, List
T = TypeVar("T")

# 退出命令
EXIT_KEYWORDS = ("q", "quit", "exit")

# 通用安全输入 
def safe_input(
        prompt: str,
        parser: Callable[[str], T],
        error_msg: str = "Input format is incorrect! Please try again.",
        exit_keywords: tuple = EXIT_KEYWORDS
        ) -> T:
    while True:
        raw = input(prompt)
        if raw.strip().lower() in exit_keywords:
            raise SystemExit(0)
        try:
            return parser(raw)
        except Exception:
            print(error_msg)

def int_input(prompt: str) -> int:
    return safe_input(prompt, int, "Please input an integer")

def float_input(prompt: str) -> float:
    return safe_input(prompt, float, "Please input a number")

def float_list_input(prompt: str) -> List[float]:
    return safe_input(prompt, lambda s: [float(_) for _ in s.split()], "Please input numbers that are separated by spaces")

def yes_or_not_input(prompt: str ="") -> bool:
    yes_set = {"y", "yes"}
    no_set  = {"n", "no"}
    while True:
        raw = input(prompt + "(Y/N)").strip().lower()
        if raw in EXIT_KEYWORDS:
            raise SystemExit(0)
        if raw in yes_set:
            return True
        if raw in no_set:
            return False
        print("Please check your input!")

def group_data_input(k: int=0) -> dict:
    """
        批量数据录入
        return {"alpha":alpha(float), "k":k(int), "data":data(dict)}
        data = {group0:[],group1:[](,...)}
    """
    # 数据输入
    alpha = float_input("Please enter the significance level: ")

    if k == 0:
        # 当输入未指定k的大小时
        k = int_input("Please enter the number of groups: ")
    data = {}
    print("Please enter the data for each group, figures should be split by space!")
    for i in range(k):
        data[f"group{i}"] = float_list_input(f"group{i}: ")

    # 数据检查
    print("\nCheck the correctness of the data\n")
    for key, group in data.items():
        print(key, ":", group)

    # 数据更改
    flag = yes_or_not_input("Do you need to correct the data?")

    if flag:
        print("If you want to change the second number in group0, then type:0, 1: 9\n" \
                    "0 here means group0, 1 means the second number while 9 stands for the correct data.")
        
        while flag:
            coord, num = input().split(":")
            try:
                num = float(num)
                x, y = [int(_) for _ in coord.split(",")][0], [int(_) for _ in coord.split(",")][1] 
                data[f'group{x}'][y] = num
            except:
                print("Input is not in the proper format!")
            flag = yes_or_not_input("Still something wrong with it?")

        print("\nAlright, the followings are the final data")
        for key, group in data.items():
            print(key, ":", group)
    return {"alpha":alpha, "k":k, "data":data}

###################
# sample variance #
###################
def get_sample_variance(data:dict) -> dict:
    res = {}
    for index, group in data.items():
        # 外层对组循环
        t, n = 0, len(group)        # t为临时变量，用于计算sample variance, n为每组的样本两
        mean = sum(group) / n
        for num in group:
            # 组内循环
            t += (num - mean) ** 2
        res[index] = t / (n - 1)    # 无偏估计
    return res

if __name__ == "__main__":
    res = get_sample_variance({"group0":[5,5,5,5,10]})
    print(res)