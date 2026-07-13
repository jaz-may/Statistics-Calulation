from scipy.stats import f
from statscalculation.cli_utils import int_input, float_input, float_list_input

def HSD(alpha: float, k: int, v: int, r: int, MSE: float, means: list[float]) -> str:
    """
    如果有显著性差异，且满足ni = nj的假设，给出HSD
    Args:
        alpha: significance level
        k: the number of groups
        v: n - k
        r: the number of data in each group(assumed the same among all groups)
        MSE: mean square error
        means: the means of each group
    """
    if MSE == 0:          # HSD无意义
        print("MSE ≈ 0, within-group variance is zero; HSD cannot be computed.")

    from math import sqrt
    from scipy.stats import studentized_range
    Q = studentized_range.ppf(1 - alpha, k, v)
    D = Q * sqrt(MSE / r)
    for i in range(k - 1):
        for j in range(i + 1, k):
            lower_bound, upper_bound = means[i] - means[j] - D, means[i] - means[j] + D
            diff = "not significantly different" if (lower_bound <= 0 <= upper_bound) else "significantly different"
            print(f"group{i} vs group{j} Tukey's HSD: ({lower_bound}, {upper_bound}) -> {diff}")
        print("HSD ends")
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
    k = int_input("Please enter the number of groups:")
    data = {}
    print("Please enter the data for each group, figures should be split by space!")
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
    
    # 新产生数据
    n = 0                           # the number of the whole data
    total = 0                       # sum of the whole data
    SSE = 0         
    counts, means = [], []          # counts: number of data within each group, means: means of data within each group 
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
    equal_size = len(set(counts)) == 1
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

    # 结论
    if p < alpha:
        print(f"p = {p:.4f} < α = {alpha}, reject H₀ ————— at least one group mean differs significantly.")
        if equal_size:
            HSD(alpha, k, n - k, counts[0], MSE, means)
    else:
        print(f"p = {p:.4f} ≥ α = {alpha}, fail to reject H₀ ————— no significant difference detected among group means.")
    
    return "\nANOVA F-test ends"

if __name__ == "__main__":
    main()