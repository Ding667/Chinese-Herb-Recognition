"""
=========================================================
YOLOv8 模型训练模块
=========================================================
"""



import os
import torch
from ultralytics import YOLO


class Trainer:

    def __init__(
            self,
            model_path: str,
            data_yaml: str,
            project: str,
            name: str
    ):

        self.model_path = model_path
        self.data_yaml = data_yaml
        self.project = project
        self.name = name

        self.model = YOLO(self.model_path)

    def check_device(self):
        """
        检查GPU
        """

        if torch.cuda.is_available():

            print("=" * 60)
            print("GPU :", torch.cuda.get_device_name(0))
            print("CUDA:", torch.version.cuda)
            print("=" * 60)

            return 0

        print("=" * 60)
        print("当前没有GPU，使用CPU训练")
        print("=" * 60)

        return "cpu"

    def check_dataset(self):

        if not os.path.exists(self.data_yaml):

            raise FileNotFoundError(
                f"没有找到数据集配置文件：{self.data_yaml}"
            )

        print("=" * 60)
        print("数据集配置：")
        print(self.data_yaml)
        print("=" * 60)

    def train(self):

        self.check_dataset()

        device = self.check_device()

        print("=" * 60)
        print("开始训练 YOLOv8 ...")
        print("=" * 60)

        self.model.train(
            # ----------------------------
            # 随机种子seed
            # ----------------------------
            seed=42,
            deterministic=True,

            # ----------------------------
            # 数据集
            # ----------------------------
            data=self.data_yaml,

            # ----------------------------
            # 模型参数
            # ----------------------------
            epochs=100,

            imgsz=768,

            batch=16,

            workers=0,

            device=device,

            # ----------------------------
            # 优化器
            # ----------------------------
            label_smoothing=0.05,

            close_mosaic=10,

            #开启余弦学习率
            cos_lr=True,

            optimizer="SGD",

            lr0=0.001,

            lrf=0.01,

            momentum=0.937,

            weight_decay=0.0008,

            warmup_epochs=5,

            warmup_momentum=0.8,

            warmup_bias_lr=0.1,

            # ----------------------------
            # 数据增强
            # ----------------------------
            hsv_h=0.02,

            hsv_s=0.8,

            hsv_v=0.5,

            translate=0.1,

            scale=0.5,

            degrees=5,

            shear=0,

            perspective=0,

            flipud=0,

            fliplr=0.5,

            mosaic=0.5,

            mixup=0.2,

            copy_paste=0,

            # ----------------------------
            # AMP
            # ----------------------------
            amp=False,

            # ----------------------------
            # 保存
            # ----------------------------
            save=True,

            save_period=10,

            exist_ok=True,

            project=self.project,

            name=self.name,

            # ----------------------------
            # 提前停止
            # ----------------------------
            patience=30,

            # ----------------------------
            # Cache
            # ----------------------------
            cache=False,

            # ----------------------------
            # 可视化
            # ----------------------------
            plots=True,

            verbose=True

        )

        print("=" * 60)
        print("训练完成")
        print("=" * 60)