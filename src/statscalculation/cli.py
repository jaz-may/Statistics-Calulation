"""
statscalculation CLI — 统一入口
"""

import argparse
from statscalculation import __version__, __author__


# ── Banner ──────────────────────────────────────────────
BANNER = f"""
  ###################################################
                   statscalculation                
                    v{__version__}               
                    by {__author__}              
  ###################################################
"""

MANUAL = f"""
      statscalculation is an interactive CLI calculator designed for
      small-sample hand-calculation scenarios in statistics coursework.
      Enter data at the prompt and get results immediately — a faster
      alternative to a scientific calculator.

      Usage:
          stats <tool>       run a specific tool directly
          stats              show this page and available tools

      Tools:
          anova  — one-way ANOVA (ANOVA table + Tukey HSD)
          ttest  — two-sample test (z-test / pooled t / Welch t)

      Type q / quit / exit at any prompt to leave safely.
  """

# ── 工具注册表 ──────────────────────────────────────────
# 格式: { "命令名": ("描述", import_path, 状态) }
# 状态: "done" | "wip" | "planned"

TOOLS = {
    "anova": (
        "one-way ANOVA — ANOVA table + Tukey HSD",
        "statscalculation.anova:main",
        "done",
    ),
    "ttest": (
        "two-sample test — z-test / pooled t / Welch t",
        "statscalculation.ttest.main",
        "done",
    ),
    "chisq": (
        "goodness-of-fit & independence test",
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
        print("not available")
    print()

    print("coming soon:")
    if wip:
        for name, (desc, _, _) in wip.items():
            print(f"  [ ] {name:<14}{desc}")
    else:
        print("not available")
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
        description="statscalculation — interactive calclulator designed for statistics",
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
            print(f"[!] tool '{args.command}' is not available")


if __name__ == "__main__":
    main()
