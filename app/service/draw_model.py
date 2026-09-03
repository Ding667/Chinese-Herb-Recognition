"""
=========================================================
YOLOv8 模型结构信息导出
=========================================================
"""

from pathlib import Path

from ultralytics import YOLO
from torchinfo import summary


class DrawModel:

    def __init__(self, weight_path):

        self.weight_path = Path(weight_path)

        if not self.weight_path.exists():
            raise FileNotFoundError(
                f"没有找到模型：{self.weight_path}"
            )

        self.model = YOLO(str(self.weight_path)).model

    def print_model(self):

        print("=" * 60)

        print("YOLOv8 网络结构")

        print("=" * 60)

        print(self.model)

    def save_summary(self):

        print("=" * 60)

        print("生成模型摘要...")

        print("=" * 60)

        info = summary(

            self.model,

            input_size=(1, 3, 640, 640),

            verbose=0,

            depth=5

        )

        save_path = self.weight_path.parent / "model_summary.txt"

        with open(save_path, "w", encoding="utf-8") as f:

            f.write(str(info))

        print("保存成功：", save_path)

    def save_model_structure(self):

        save_path = self.weight_path.parent / "model_structure.txt"

        with open(save_path, "w", encoding="utf-8") as f:

            f.write(str(self.model))

        print("模型结构保存成功")

    def draw(self):

        self.print_model()

        self.save_summary()

        self.save_model_structure()

        print("=" * 60)

        print("模型信息导出完成")

        print("=" * 60)


if __name__ == "__main__":

    drawer = DrawModel(

        r"runs/Chinese_Herb/weights/best.pt"

    )

    drawer.draw()