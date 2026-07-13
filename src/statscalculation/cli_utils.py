"""
CLI中输入异常处理工具
"""
from typing import Callable, TypeVar, List
T = TypeVar("T")

def safe_input(
        prompt: str,
        parser: Callable[[str], T],
        error_msg: str = "Input format is incorrect! Please try again.",
        exit_keywords: tuple = ("q", "quit", "exit")
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
    return safe_input(prompt, lambda s: [float(_) for _ in s.split()], "Please input numbers that are seperated by space")