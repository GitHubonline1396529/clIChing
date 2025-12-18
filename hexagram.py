"""
name: hexagram.py
date: 2025-12-08
author: githubonline1396529
description: Hexagram generation and manipulation for I Ching divination.
"""

import random
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class Yao:
    value: bool  # 0: Yin, 1: Yang.
    changing: bool  # Whether to be changeable (for old Yin/Yang).
    coins: Tuple[int, int, int]  # Result of the three coins.

    def display(self, colored=True) -> str:
        """Display the Yao hexagram."""
        from display import colored_yao

        if colored:
            return colored_yao(self.coins, self.value, self.changing)
        else:
            # No-color display.
            if self.value == 0:  # 阴爻
                return "### ###" if self.changing else "#######"
            else:  # 阳爻
                return "#######" if self.changing else "### ###"


class Hexagram:
    def __init__(self, yaos: List[Yao]):
        self.yaos = yaos  # 从下往上：[初爻, 二爻, 三爻, 四爻, 五爻, 上爻]
        self._calculate_hexagram()

    def _calculate_hexagram(self):
        """计算卦的编号和二进制表示"""
        # 计算编号：初爻为最低位，上爻为最高位
        self.original_number = 0
        for i, yao in enumerate(self.yaos):  # i从0到5，对应初爻到上爻
            if yao.value == 1:
                self.original_number += 1 << i  # 2的i次方

        # 生成从上爻到初爻的二进制字符串（6位，不足补0）
        self.original_binary = format(self.original_number, "06b")

    def display(self, colored=True):
        """显示卦象（从上往下）"""
        for i in range(5, -1, -1):  # 从上爻(6)到初爻(1)
            yao = self.yaos[i]
            print(yao.display(colored))

    def get_changing_hexagram(self, positions: List[int]) -> "Hexagram":
        """根据指定爻位生成变卦

        Args:
            positions: 要变化的爻位列表 (1-6)

        Returns:
            新的Hexagram对象（变卦）
        """
        new_yaos = []
        for idx, yao in enumerate(self.yaos):
            position = idx + 1  # 爻位（1-6）

            # Judge if the user's input is within 1~6.
            if position in positions and yao.changing:
                # 变爻：老阴变少阳，老阳变少阴
                # Exchange Yin and Yang.
                new_value = 1 if yao.value == 0 else 0
                # 生成新的硬币结果（符合变化后的阴阳）
                if new_value == 0:  # 变为少阴
                    new_coins = (0, 1, 1)  # 两个 1 一个 0
                else:  # 变为少阳
                    new_coins = (1, 0, 0)  # 两个 0 一个 1
                new_changing = False  # 变后为少阴少阳，不再可变
            else:
                # 不变爻
                new_value = yao.value
                new_coins = yao.coins
                new_changing = yao.changing

            new_yaos.append(Yao(new_value, new_changing, new_coins))

        return Hexagram(new_yaos)

    def _get_data_path(self, filename: str) -> Path:
        """获取数据文件路径"""
        return Path(__file__).parent / "data" / "hexagrams" / filename

    def get_interpretation(self, hexagram_number: int) -> str:
        """读取卦辞文件"""
        filepath = self._get_data_path(f"{hexagram_number:02d}.txt")
        if filepath.exists():
            try:
                return filepath.read_text(encoding="utf-8")
            except:
                return filepath.read_text(encoding="gbk")
        return f"卦辞文件 {hexagram_number:02d}.txt 未找到"

    def display_interpretation(self):
        """显示卦辞"""
        print(self.get_interpretation(self.original_number))


def generate_hexagram() -> Hexagram:
    """生成六爻卦象"""
    yaos = []
    for _ in range(6):
        coins = tuple(random.randint(0, 1) for _ in range(3))
        sum_coins = sum(coins)

        # 根据规则判断爻象
        if sum_coins == 0:  # 三个0 -> 老阴（可变）
            yao = Yao(0, True, coins)
        elif sum_coins == 1:  # 两个0一个1 -> 少阳（不可变）
            yao = Yao(1, False, coins)
        elif sum_coins == 2:  # 两个1一个0 -> 少阴（不可变）
            yao = Yao(0, False, coins)
        else:  # 三个1 -> 老阳（可变）
            yao = Yao(1, True, coins)

        yaos.append(yao)

    return Hexagram(yaos)
