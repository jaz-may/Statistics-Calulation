# statscalculation

写着玩的古法编程项目。命令行交互式统计计算器，用于手算小样本统计数据（如数理统计作业）。

已上传至 [PyPI](https://pypi.org/project/statscalculation/)。

## 安装

```bash
pip install statscalculation
```

## 使用

```bash
stat           # 查看可用工具
stat anova     # 单因素方差分析
stat ttest     # 双样本检验（z / pooled t / Welch t）
```

或直接启动：

```bash
anova
ttest
```

任意输入处键入 `q` / `quit` / `exit` 退出。

## 工具

| 命令 | 说明 |
|------|------|
| `anova` | 单因素方差分析 + Tukey HSD 事后比较 |
| `ttest` | 双样本检验：z 检验 / pooled t / Welch t，输出决策表与 p 值 |
