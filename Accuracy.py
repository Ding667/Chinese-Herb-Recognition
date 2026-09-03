# -*- coding: utf-8 -*-
"""Top-1 / Top-5 分类准确率统计脚本
在验证集上统计模型的 Top-1 与 Top-5 分类准确率，评估整图级识别能力。
"""
import os
from pathlib import Path
from collections import defaultdict

import yaml
from ultralytics import YOLO

# 项目根目录（本脚本所在目录）
ROOT = Path(__file__).resolve().parent

# 模型路径
MODEL_PATH = ROOT / "weights" / "best.pt"

# 通过 data.yaml 获取数据集路径，支持跨机器迁移
DATA_YAML = ROOT / "100种中药分类数据集" / "data" / "data.yaml"
_data_cfg = yaml.safe_load(open(DATA_YAML, encoding="utf-8"))
_data_root = Path(_data_cfg["path"])
if not _data_root.is_absolute():
    _data_root = (ROOT / _data_root).resolve()
VAL_IMAGES = _data_root / _data_cfg["val"]
VAL_LABELS = _data_root / _data_cfg["val"].replace("images", "labels")


def check_paths():
    """路径检查：模型或数据目录不存在时明确报错"""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"模型不存在：{MODEL_PATH}")
    if not VAL_IMAGES.exists():
        raise FileNotFoundError(f"验证集图片目录不存在：{VAL_IMAGES}")
    if not VAL_LABELS.exists():
        raise FileNotFoundError(f"验证集标签目录不存在：{VAL_LABELS}")


check_paths()

model = YOLO(str(MODEL_PATH))

top1_correct = 0
top5_correct = 0
total = 0

image_list = []

for root, _, files in os.walk(VAL_IMAGES):
    for file in files:
        if file.lower().endswith((".jpg", ".png", ".jpeg", ".bmp")):
            image_list.append(os.path.join(root, file))

# 图片数量为 0 时明确提示
if len(image_list) == 0:
    raise RuntimeError(f"验证集图片数量为 0，请检查目录：{VAL_IMAGES}")

print(f"验证图片数量：{len(image_list)}")

for img_path in image_list:
    # 由图片路径推导对应标签路径（images → labels）
    label_path = img_path.replace("images", "labels")
    label_path = os.path.splitext(label_path)[0] + ".txt"

    if not os.path.exists(label_path):
        continue

    with open(label_path, "r") as f:
        lines = f.readlines()

    if len(lines) == 0:
        continue

    gt = int(lines[0].split()[0])

    results = model.predict(
        img_path,
        verbose=False,
        conf=0.001,
        max_det=300
    )

    result = results[0]

    if len(result.boxes) == 0:
        total += 1
        continue

    score = defaultdict(float)

    for cls, conf in zip(result.boxes.cls.cpu().numpy(),
                         result.boxes.conf.cpu().numpy()):
        cls = int(cls)
        if conf > score[cls]:
            score[cls] = conf

    pred = sorted(score.items(),
                  key=lambda x: x[1],
                  reverse=True)

    pred_cls = [x[0] for x in pred]

    total += 1

    # Top-1：置信度最高的预测类别与真实类别一致
    if len(pred_cls) > 0:
        if pred_cls[0] == gt:
            top1_correct += 1

    # Top-5：真实类别出现在置信度前 5 的预测中
    if gt in pred_cls[:5]:
        top5_correct += 1

print("=" * 60)

print("Top1 Accuracy : {:.2f}%".format(
    top1_correct / total * 100))

print("Top5 Accuracy : {:.2f}%".format(
    top5_correct / total * 100))

print("=" * 60)
