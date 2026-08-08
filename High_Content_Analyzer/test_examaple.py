import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import skimage
import pytest
import pygame
import simpy as smp
import cv2
print(cv2.__version__)

import matplotlib.pyplot as plt
# 设置显示中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

labels = [
    "肿瘤学 (19%)", "药物筛选与平台 (23%)", "感染性疾病 (10%)",
    "神经科学 (8%)", "基础细胞与代谢 (8%)", "心血管与纤维化 (6%)",
    "毒理学与安全 (6%)", "免疫学与炎症 (4%)", "干细胞(4%)",
    "衰老与年龄相关 (4%)", "肌肉骨骼 (2%)", "其他 (6%)"
]
sizes = [19, 23, 10, 8, 8, 6, 6, 4, 4, 4, 2, 6]
colors = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD",
    "#FFA07A", "#87CEEB", "#98FB98", "#F4A460", "#C0C0C0", "#A9A9A9"
]

fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, autopct="%1.0f%%", startangle=140,
    colors=colors, pctdistance=0.80, labeldistance=1.18
)
for autotext in autotexts:
    autotext.set_color("white")
    autotext.set_fontweight("bold")
    autotext.set_fontsize(9)
ax.set_title("高内涵成像在各领域应用比例（最近一年 NCBI 文献外推）", fontsize=15, pad=20)
plt.tight_layout()
plt.savefig("hci_pie.png", dpi=300, bbox_inches="tight")
plt.show()

print("Hello, this is a test script for data analysis.")