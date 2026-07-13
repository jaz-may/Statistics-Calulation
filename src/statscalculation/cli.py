"""
statscalculation CLI — 统一入口
"""

import argparse
from statscalculation import __version__, __author__


# ── Banner ──────────────────────────────────────────────
BANNER = r"""
  ╔══════════════════════════════════════════════════╗
  ║                 statscalculation                 ║
  ║                   v{version}                     ║
  ║                   by {author}                    ║
  ╚══════════════════════════════════════════════════╝
""".format(version=__version__, author=__author__)

MANUAL = """
    简介:
    statscalculation 是一个交互式 CLI 统计计算器，专为小样本手算场景设计。
    不需要准备 Excel / CSV 文件，直接在终端输入数据即可得到检验结果。
    目标是替代科学计算器在数理统计作业中的繁琐操作。

    用法:
    stats <子命令>       运行指定工具
    stats anova          运行单因素方差分析

    也可以跳过统一入口，直接敲子命令名:
    anova                效果等同于 stats anova

    在任意工具的输入提示处键入 q / quit / exit 均可安全退出。
""".format(version=__version__, author=__author__)

# ── 工具注册表 ──────────────────────────────────────────
# 格式: { "命令名": ("描述", import_path, 状态) }
# 状态: "done" | "wip" | "planned"

TOOLS = {
    "anova": (
        "单因素方差分析 — 含 ANOVA 表输出、显著性判断",
        "statscalculation.anova:main",
        "done",
    ),
    "ttest": (
        "双样本 t 检验 — 方差已知 / 未知相等 / 未知不等",
        None,
        "wip",
    ),
    "chisq": (
        "拟合优度检验 & 列联表独立性检验",
        None,
        "wip",
    ),
    "regression": (
        "简单线性回归 — 系数估计、显著性检验",
        None,
        "wip",
    ),
}


def print_banner():
    print(BANNER)
    print(MANUAL)


def _show_tools():
    """打印可用工具列表"""
    # 已完成的
    done = {k: v for k, v in TOOLS.items() if v[2] == "done"}
    wip = {k: v for k, v in TOOLS.items() if v[2] == "wip"}

    print("ready:")
    if done:
        for name, (desc, _, _) in done.items():
            print(f"{name:<14}{desc}")
    else:
        print("not avaliable")
    print()

    print("coming soon:")
    if wip:
        for name, (desc, _, _) in wip.items():
            print(f"  [ ] {name:<14}{desc}")
    else:
        print("not avaliable")
    print()


def _import_tool(tool_path: str):
    """按 'module:function' 路径动态导入工具入口函数"""
    if tool_path is None:
        return None
    module_path, func_name = tool_path.split(":")
    import importlib
    mod = importlib.import_module(module_path)
    return getattr(mod, func_name)


def main():
    # 构建 argparse，动态注册已实现工具为子命令
    parser = argparse.ArgumentParser(
        prog="stats",
        description="statscalculation — 交互式数理统计计算器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    sub = parser.add_subparsers(dest="command", title="子命令")

    done_tools = {k: v for k, v in TOOLS.items() if v[2] == "done"}
    for name, (desc, _, _) in done_tools.items():
        sub.add_parser(name, help=desc)

    args = parser.parse_args()

    if args.command is None:
        print_banner()
        _show_tools()
    else:
        tool_info = TOOLS.get(args.command)
        if tool_info and tool_info[1] is not None:
            func = _import_tool(tool_info[1])
            if func:
                func()
            else:
                print(f"[!] tool '{args.command}' goes wrong")
        else:
            print(f"[!] tool '{args.command}' is not avaliable")


if __name__ == "__main__":
    main()
