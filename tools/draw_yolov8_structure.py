# -*- coding: utf-8 -*-
"""绘制 YOLOv8 简化网络结构示意图（论文用图）"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#409eff"
DARK = "#2c3e50"
LIGHT = "#ecf5ff"
GREEN = "#67c23a"
ORANGE = "#e6a23c"

fig, ax = plt.subplots(figsize=(8.2, 11), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis("off")


def box(x, y, w, h, text, fc=LIGHT, ec=BLUE, fs=13, tc=DARK):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12",
                       fc=fc, ec=ec, lw=1.6)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=tc, weight="bold")


def arrow(x1, y1, x2, y2, color=BLUE):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                        mutation_scale=22, lw=2.2, color=color)
    ax.add_patch(a)


# ===== 1. 输入 =====
box(3.1, 13.0, 3.8, 0.8, "输入图像\n(768×768×3)", fc="#f0f9eb", ec=GREEN, fs=13)
arrow(5.0, 13.0, 5.0, 12.4)

# ===== 2. Backbone =====
box(0.5, 8.2, 9.0, 4.2, "", fc="none", ec=DARK, fs=0)
ax.text(5.0, 12.15, "Backbone 骨干网络", ha="center", fontsize=14,
        color=DARK, weight="bold")
box(0.9, 8.5, 1.7, 1.1, "Conv\n卷积")
box(2.9, 8.5, 1.7, 1.1, "C2f\n特征模块")
box(4.9, 8.5, 1.7, 1.1, "C2f\n特征模块")
box(6.9, 8.5, 1.7, 1.1, "SPPF\n金字塔池化")
arrow(2.6, 9.05, 2.9, 9.05)
arrow(4.6, 9.05, 4.9, 9.05)
arrow(6.6, 9.05, 6.9, 9.05)
arrow(5.0, 8.5, 5.0, 7.9)

# ===== 3. Neck =====
box(0.5, 5.2, 9.0, 2.7, "", fc="none", ec=DARK, fs=0)
ax.text(5.0, 7.65, "Neck 颈部网络", ha="center", fontsize=14,
        color=DARK, weight="bold")
box(0.9, 5.5, 3.9, 1.1, "FPN 特征金字塔\n(自顶向下传递语义)")
box(5.2, 5.5, 3.9, 1.1, "PAN 路径聚合\n(自底向上传递定位)")
arrow(3.2, 5.5, 4.4, 5.5)
arrow(5.0, 5.2, 5.0, 4.6)

# ===== 4. Head =====
box(0.5, 2.2, 9.0, 2.4, "", fc="none", ec=DARK, fs=0)
ax.text(5.0, 4.35, "Detection Head 检测头", ha="center", fontsize=14,
        color=DARK, weight="bold")
box(1.1, 2.5, 3.5, 1.0, "分类分支\n(类别预测)")
box(5.4, 2.5, 3.5, 1.0, "回归分支\n(边界框预测)", fc="#fdf6ec", ec=ORANGE)
arrow(2.85, 2.5, 2.85, 2.0, color=ORANGE)
arrow(7.15, 2.5, 7.15, 2.0, color=ORANGE)

# ===== 5. 输出 =====
box(1.8, 0.5, 6.4, 1.2, "输出：药材类别 + 置信度 + 边界框坐标\n(100 类中草药检测)",
    fc="#f56c6c", ec="#f56c6c", fs=13, tc="white")

plt.tight_layout()
plt.savefig("results/yolov8_structure.png", bbox_inches="tight", dpi=300)
print("已保存 results/yolov8_structure.png")
