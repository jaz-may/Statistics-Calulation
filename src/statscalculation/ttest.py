"""
    two sample test
"""
from statscalculation.cli_utils import int_input, float_input, float_list_input, yes_or_not_input, group_data_input, get_sample_variance
from math import sqrt
from scipy.stats import norm, t as t_dist

def test_table(stat, crit_alpha, crit_half, dist="z", df=None) -> None:
    """
        打印双样本检验决策表（z 检验 / t 检验通用）
        dist: "z" 或 "t"
        df:   自由度（仅 t 检验需要）
    """
    if dist == "z":
        p_right = norm.sf(stat)           # P(Z ≥ z)
        p_left  = norm.cdf(stat)          # P(Z ≤ z)
        p_two   = 2 * norm.sf(abs(stat))  # 2P(Z ≥ |z|)
    else:  # "t"
        p_right = t_dist.sf(stat, df)           # P(T ≥ t)
        p_left  = t_dist.cdf(stat, df)          # P(T ≤ t)
        p_two   = 2 * t_dist.sf(abs(stat), df)  # 2P(T ≥ |t|)

    # 判断拒绝与否
    rej_right = "Reject H₀ ✓" if stat >= crit_alpha else "Fail to reject"
    rej_left  = "Reject H₀ ✓" if stat <= -crit_alpha else "Fail to reject"
    rej_two   = "Reject H₀ ✓" if abs(stat) >= crit_half else "Fail to reject"

    print(f"{'Alternative Hypothesis':>25} {'Decision':>18} {'p-value':>10}")
    print(f"{'─'*25} {'─'*18} {'─'*10}")
    print(f"{'H₁: μ_X > μ_Y':>25} {rej_right:>18} {p_right:>10.4f}")
    print(f"{'H₁: μ_X < μ_Y':>25} {rej_left:>18} {p_left:>10.4f}")
    print(f"{'H₁: μ_X ≠ μ_Y':>25} {rej_two:>18} {p_two:>10.4f}")
    print()

def main():
    """
        1.方差已知
        2.方差未知但认为相等
        3.方差未知且不相等
    """
    # 数据输入
    group_data = group_data_input(k = 2)
    alpha, data = group_data["alpha"], group_data["data"]
    n, m = len(data["group0"]), len(data["group1"])                     # m为group0的数据量， n为group1的数据量
    mean_X, mean_Y = sum(data["group0"]) / n, sum(data["group1"]) / m   # 分别计算两组的平均值

    # 判断属于哪一种情况
    var_known = yes_or_not_input("Are the variances known?")
    if var_known:
        # 方差已知 -> z test statistics
        
        # 构造临界值
        z_alpha = norm.ppf(1 - alpha)
        z_half = norm.ppf(1 - alpha / 2)
        
        # 构建z统计量
        var_X = float_input("Please enter the variance of group0: ")
        var_Y = float_input("Please enter the variance of group1: ")
        
        Z = (mean_X - mean_Y) / sqrt(var_X / m + var_Y / n)
        
        # 打印结果
        print(f"Z = {Z:.4f},  zα = {z_alpha:.4f},  zα/₂ = {z_half:.4f}")
        print()
        test_table(Z, z_alpha, z_half, dist="z")
        
    else:
        # 方差未知
        var_equal = yes_or_not_input("Are the variances equal?")
        var_X, var_Y = get_sample_variance(data)["group0"], get_sample_variance(data)["group1"]
        if var_equal:

            # 方差未知且相等 -> pooled t test
            s2_pooled = ((n - 1) * var_X + (m - 1) * var_Y) / (n + m - 2)
            df = n + m - 2

            # t 临界值
            t_alpha = t_dist.ppf(1 - alpha, df)
            t_half  = t_dist.ppf(1 - alpha / 2, df)

            # t 统计量
            t_stat = (mean_X - mean_Y) / sqrt(s2_pooled * (1 / n + 1 / m))

            # 打印结果
            print(f"T = {t_stat:.4f}, tα = {t_alpha:.4f}, tα/₂ = {t_half:.4f},  df = {df}")
            print()
            test_table(t_stat, t_alpha, t_half, dist="t", df=df)
        else:
            # 方差未知且不相等 -> Welch t test
            # welch统计量
            v = round((var_X / n + var_Y / m) ** 2 / (((var_X / n) ** 2 / (n - 1)) + ((var_Y / m) ** 2 / (m - 1))))    # Satterthwaite 近似自由度
            w_stat = (mean_X - mean_Y) / sqrt(var_X / n + var_Y / m)                                                  # Welch t 统计量

            # t 临界值
            t_alpha = t_dist.ppf(1 - alpha, v)
            t_half  = t_dist.ppf(1 - alpha / 2, v)

            # 打印结果
            print(f"Welch T = {w_stat:.4f},  tα = {t_alpha:.4f},  tα/₂ = {t_half:.4f},  df ≈ {v}")
            print()
            test_table(w_stat, t_alpha, t_half, dist="t", df=v)

if __name__ == "__main__":
    main()