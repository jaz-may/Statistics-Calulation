from scipy.stats import f
from statscalculation.cli_utils import int_input, float_input, float_list_input

def HSD():
    """
    如果有显著性差异，就给出HSD
    """
    return 


def main():
    """
    #                df      SS      MS      F       P
    #Treatment      k-1     SSTR    MSTR  MSTR/MSE
    #Error          n-k      SSE     MSE 
    #Total          n-1    SSTOT 

    """
# 数据输入
    alpha = float_input("Please enter the significance level:")
    k = int_input("Please enter the number og groups:")
    data = {}

    print("Please input the data for each group, figures should be split by space!")
    for i in range(k):
        data[f"group{i}"] = float_list_input(f"group{i}:")

    # 数据检查
    print("\nCheck the correctness of the data\n")
    for key, group in data.items():
        print(key, ":", group)

    # 数据更改
    flag = input("Do you need to correct the data? (Y/N)\n").lower()

    if flag == "y" or flag == "yes":
        
        print("If you want to change the second number in group0, then type:0, 15: 9\n" \
                    "0 here means group0, 1 means the second number while 9 stands for the correct data.")
        
        while flag == "y" or flag == "yes":
            coord, num = input().split(":")
            try:
                num = float(num)
                x, y = [int(_) for _ in coord.split(",")][0], [int(_) for _ in coord.split(",")][1] 
                data[f'group{x}'][y] = num
            except:
                print("Input is not in the proper format!")
            flag = input("Still something wrong with it? (Y/N)\n").lower()

        print("\nAlright, the followings are the final data")
        for key, group in data.items():
            print(key, ":", group)
    n = 0
    total = 0
    SSE = 0
    counts, means = [], []
    for key, group in data.items():
        nj = len(group)
        n += nj
        mean = sum(group) / nj
        total += sum(group)

        # SSE
        SSE += sum([(num - mean) ** 2 for num in group])

        counts.append(nj)
        means.append(mean)

    sample_mean = total / n

    # SSTR
    SSTR = 0 
    for i in range(len(means)):
        SSTR += counts[i] * ((means[i] - sample_mean) ** 2)

    # MSTR
    MSTR = SSTR / (k - 1)

    # MSE
    MSE = SSE / (n - k)

    # SSTOT
    SSTOT = SSE + SSTR

    # F 
    F = MSTR / MSE

    # P
    p = 1 - f.cdf(F, k - 1, n - k)  

    print(f"{'':>15} {'df':>6} {'SS':>25} {'MS':>25} {'F':>25} {'p':>6}")
    print(f"{'Treatment':>15} {k-1:>6} {SSTR:>25.2f} {MSTR:>25.2f} {MSTR/MSE:>25.2f} {p:>6.2f}")
    print(f"{'Error':>15} {n-k:>6} {SSE:>25.2f} {MSE:>25.2f}")
    print(f"{'Total':>15} {n-1:>6} {SSTOT:>25.2f}")

    print("\n")
    if p < alpha:
        print(f"p = {p:.4f} < α = {alpha}, reject H₀ ————— at least one group mean differs significantly.")
    else:
        print(f"p = {p:.4f} ≥ α = {alpha}, fail to reject H₀ ————— no significant difference detected among group means.")
    
    return "\nANOVA F-test ends"

if __name__ == "__main__":
    main()