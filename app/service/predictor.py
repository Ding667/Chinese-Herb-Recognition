"""
=========================================================
YOLOv8 中草药识别预测模块
项目：基于轻量化图像检测算法的中草药识别系统
=========================================================
"""

from pathlib import Path
from typing import List, Dict

import cv2
from ultralytics import YOLO


class Predictor:

    def __init__(self, weight_path: str):

        self.weight_path = Path(weight_path)

        if not self.weight_path.exists():
            raise FileNotFoundError(
                f"模型不存在：{self.weight_path}"
            )

        print("=" * 60)
        print("正在加载YOLO模型...")
        print("=" * 60)

        self.model = YOLO(str(self.weight_path))

        print("模型加载成功！")

    # ---------------------------------------------------
    # 图片预测
    # ---------------------------------------------------
    def predict(
            self,
            image_path: str,
            conf=0.25,
            save=True
    ) -> Dict:

        results = self.model.predict(

            source=image_path,

            conf=conf,

            imgsz=640,

            save=save,

            project="runs",

            name="predict",

            exist_ok=True,

            verbose=False

        )

        result = results[0]

        boxes = []

        names = self.model.names

        for box in result.boxes:

            cls = int(box.cls)

            score = float(box.conf)

            x1, y1, x2, y2 = map(float, box.xyxy[0])

            boxes.append({

                "class_id": cls,

                "class_name": names[cls],

                "confidence": round(score, 4),

                "bbox": [

                    round(x1, 2),

                    round(y1, 2),

                    round(x2, 2),

                    round(y2, 2)

                ]

            })

        return {

            "image": image_path,

            "count": len(boxes),

            "results": boxes

        }

    # ---------------------------------------------------
    # 返回带检测框图片
    # ---------------------------------------------------
    def predict_and_save(

            self,

            image_path,

            save_path

    ):

        result = self.model.predict(

            source=image_path,

            save=False,

            verbose=False

        )[0]

        image = result.plot()

        cv2.imwrite(save_path, image)

        return save_path

    # ---------------------------------------------------
    # 批量预测
    # ---------------------------------------------------
    def predict_folder(

            self,

            folder

    ):

        folder = Path(folder)

        results = []

        for img in folder.iterdir():

            if img.suffix.lower() in [

                ".jpg",

                ".jpeg",

                ".png",

                ".bmp"

            ]:

                results.append(

                    self.predict(str(img))

                )

        return results

    # ---------------------------------------------------
    # 获取类别
    # ---------------------------------------------------
    def get_classes(self) -> List[str]:

        return list(self.model.names.values())

    # ---------------------------------------------------
    # 获取类别数量
    # ---------------------------------------------------
    def class_count(self):

        return len(self.model.names)


if __name__ == "__main__":

    predictor = Predictor(

        r"runs/Chinese_Herb/weights/best.pt"

    )

    result = predictor.predict(

        r"test.jpg"

    )

    print(result)


# 返回的数据格式（FastAPI 会直接使用）
# {
#   "image": "test.jpg",
#   "count": 2,
#   "results": [
#     {
#       "class_id": 12,
#       "class_name": "黄芪",
#       "confidence": 0.9876,
#       "bbox": [
#         123.5,
#         55.4,
#         310.8,
#         288.9
#       ]
#     },
#     {
#       "class_id": 35,
#       "class_name": "当归",
#       "confidence": 0.9654,
#       "bbox": [
#         360.2,
#         80.3,
#         540.7,
#         330.5
#       ]
#     }
#   ]
# }
# 以后 FastAPI 就直接调用
#
# 例如：
#
# predictor.predict(image_path)
#
# 返回的就是：
#
# {
#     "count":2,
#     "results":[...]
# }