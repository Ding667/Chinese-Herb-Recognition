"""
=========================================================
YOLOv8 模型评估模块
=========================================================
"""

from pathlib import Path
from ultralytics import YOLO


class Evaluator:
    """
    YOLOv8 模型评估
    """

    def __init__(self, weight_path: str):

        self.weight_path = Path(weight_path)

        if not self.weight_path.exists():
            raise FileNotFoundError(f"模型不存在：{self.weight_path}")

        self.model = YOLO(str(self.weight_path))

    def evaluate(
            self,
            imgsz=640,
            batch=16,
            device=0,
            conf=0.25,
            iou=0.7
    ):
        """
        验证模型
        """

        print("=" * 60)
        print("开始模型验证...")
        print("=" * 60)

        metrics = self.model.val(

            imgsz=imgsz,

            batch=batch,

            device=device,

            conf=conf,

            iou=iou,

            plots=True,

            save_json=False,

            verbose=True

        )

        print("\n================== 评估结果 ==================")

        print(f"Precision      : {metrics.box.mp:.4f}")

        print(f"Recall         : {metrics.box.mr:.4f}")

        print(f"mAP@0.5        : {metrics.box.map50:.4f}")

        print(f"mAP@0.5:0.95   : {metrics.box.map:.4f}")

        print("=============================================\n")

        return {
            "precision": metrics.box.mp,
            "recall": metrics.box.mr,
            "map50": metrics.box.map50,
            "map5095": metrics.box.map
        }

    def print_class_result(self):
        """
        输出每个类别AP
        """

        metrics = self.model.val(verbose=False)

        names = self.model.names

        ap50 = metrics.box.maps

        print("=" * 60)
        print("各类别 AP")
        print("=" * 60)

        for i, value in enumerate(ap50):

            print(f"{i:03d}  {names[i]:20s}  AP={value:.4f}")

        print("=" * 60)


if __name__ == "__main__":

    evaluator = Evaluator(

        r"runs/Chinese_Herb/weights/best.pt"

    )

    evaluator.evaluate()

    # 输出100个中草药类别AP
    evaluator.print_class_result()