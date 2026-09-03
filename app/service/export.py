"""
=========================================================
YOLOv8 模型导出模块
支持：
    1. ONNX
    2. TorchScript
    3. OpenVINO
=========================================================
"""

from pathlib import Path
from ultralytics import YOLO


class Exporter:

    def __init__(self, weight_path):

        self.weight_path = Path(weight_path)

        if not self.weight_path.exists():
            raise FileNotFoundError(
                f"模型不存在：{self.weight_path}"
            )

        self.model = YOLO(str(self.weight_path))

    # -------------------------------
    # 导出ONNX
    # -------------------------------
    def export_onnx(self):

        print("=" * 60)
        print("开始导出 ONNX ...")
        print("=" * 60)

        self.model.export(

            format="onnx",

            imgsz=640,

            simplify=True,

            opset=12,

            dynamic=False

        )

        print("ONNX 导出完成")

    # -------------------------------
    # 导出TorchScript
    # -------------------------------
    def export_torchscript(self):

        print("=" * 60)
        print("开始导出 TorchScript ...")
        print("=" * 60)

        self.model.export(

            format="torchscript",

            imgsz=640

        )

        print("TorchScript 导出完成")

    # -------------------------------
    # 导出OpenVINO
    # -------------------------------
    def export_openvino(self):

        print("=" * 60)
        print("开始导出 OpenVINO ...")
        print("=" * 60)

        self.model.export(

            format="openvino",

            imgsz=640

        )

        print("OpenVINO 导出完成")

    # -------------------------------
    # 全部导出
    # -------------------------------
    def export(self):

        self.export_onnx()

        self.export_torchscript()

        self.export_openvino()

        print("=" * 60)
        print("全部模型导出完成")
        print("=" * 60)


if __name__ == "__main__":

    exporter = Exporter(

        r"runs/Chinese_Herb/weights/best.pt"

    )

    exporter.export()