"""
=========================================================
YOLOv8 训练结果可视化
=========================================================
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


class DrawResults:

    def __init__(self, run_dir):

        self.run_dir = Path(run_dir)

        self.csv_path = self.run_dir / "results.csv"

        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"没有找到 results.csv\n{self.csv_path}"
            )

        self.data = pd.read_csv(self.csv_path)

        # 中文支持
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False

    # ====================================================
    # Loss
    # ====================================================

    def draw_loss(self):

        plt.figure(figsize=(10, 6))

        plt.plot(
            self.data["epoch"],
            self.data["train/box_loss"],
            label="Train Box Loss"
        )

        plt.plot(
            self.data["epoch"],
            self.data["train/cls_loss"],
            label="Train Class Loss"
        )

        plt.plot(
            self.data["epoch"],
            self.data["train/dfl_loss"],
            label="Train DFL Loss"
        )

        plt.xlabel("Epoch")

        plt.ylabel("Loss")

        plt.title("Training Loss")

        plt.grid(True)

        plt.legend()

        plt.tight_layout()

        plt.savefig(

            self.run_dir / "Training_Loss.png",

            dpi=300

        )

        plt.close()

    # ====================================================
    # Validation Loss
    # ====================================================

    def draw_val_loss(self):

        plt.figure(figsize=(10, 6))

        plt.plot(

            self.data["epoch"],

            self.data["val/box_loss"],

            label="Val Box Loss"

        )

        plt.plot(

            self.data["epoch"],

            self.data["val/cls_loss"],

            label="Val Class Loss"

        )

        plt.plot(

            self.data["epoch"],

            self.data["val/dfl_loss"],

            label="Val DFL Loss"

        )

        plt.xlabel("Epoch")

        plt.ylabel("Loss")

        plt.title("Validation Loss")

        plt.grid(True)

        plt.legend()

        plt.tight_layout()

        plt.savefig(

            self.run_dir / "Validation_Loss.png",

            dpi=300

        )

        plt.close()

    # ====================================================
    # Precision Recall
    # ====================================================

    def draw_precision_recall(self):

        plt.figure(figsize=(10, 6))

        plt.plot(

            self.data["epoch"],

            self.data["metrics/precision(B)"],

            label="Precision"

        )

        plt.plot(

            self.data["epoch"],

            self.data["metrics/recall(B)"],

            label="Recall"

        )

        plt.xlabel("Epoch")

        plt.ylabel("Value")

        plt.title("Precision & Recall")

        plt.grid(True)

        plt.legend()

        plt.tight_layout()

        plt.savefig(

            self.run_dir / "Precision_Recall.png",

            dpi=300

        )

        plt.close()

    # ====================================================
    # mAP
    # ====================================================

    def draw_map(self):

        plt.figure(figsize=(10, 6))

        plt.plot(

            self.data["epoch"],

            self.data["metrics/mAP50(B)"],

            label="mAP@0.5"

        )

        plt.plot(

            self.data["epoch"],

            self.data["metrics/mAP50-95(B)"],

            label="mAP@0.5:0.95"

        )

        plt.xlabel("Epoch")

        plt.ylabel("mAP")

        plt.title("mAP Curve")

        plt.grid(True)

        plt.legend()

        plt.tight_layout()

        plt.savefig(

            self.run_dir / "mAP.png",

            dpi=300

        )

        plt.close()

    # ====================================================
    # Learning Rate
    # ====================================================

    def draw_lr(self):

        if "lr/pg0" not in self.data.columns:
            return

        plt.figure(figsize=(10, 6))

        plt.plot(

            self.data["epoch"],

            self.data["lr/pg0"],

            label="Learning Rate"

        )

        plt.xlabel("Epoch")

        plt.ylabel("LR")

        plt.title("Learning Rate")

        plt.grid(True)

        plt.legend()

        plt.tight_layout()

        plt.savefig(

            self.run_dir / "Learning_Rate.png",

            dpi=300

        )

        plt.close()

    # ====================================================
    # 总入口
    # ====================================================

    def draw(self):

        print("=" * 60)
        print("开始绘制训练曲线...")
        print("=" * 60)

        self.draw_loss()

        self.draw_val_loss()

        self.draw_precision_recall()

        self.draw_map()

        self.draw_lr()

        print("=" * 60)
        print("绘制完成")
        print("=" * 60)


if __name__ == "__main__":

    drawer = DrawResults(

        r"runs/Chinese_Herb"

    )

    drawer.draw()