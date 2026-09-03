# -*- coding: utf-8 -*-
"""YOLOv8n vs YOLOv8s 对比实验脚本
在完全一致的训练配置下分别训练 YOLOv8n 与 YOLOv8s，输出参数量与精度对比。
训练结果保存到 runs/compare/{yolov8n,yolov8s}，不覆盖 weights/best.pt。
"""
import argparse
from pathlib import Path

from ultralytics import YOLO

# 项目根目录（experiments/ 的上一级）
ROOT = Path(__file__).resolve().parent.parent

# 数据集路径
DATA = str(ROOT / "100种中药分类数据集" / "data" / "data.yaml")

# 统一训练配置（论文最终策略，两组一致）
COMMON = dict(
    data=DATA,
    epochs=100,
    imgsz=768,
    batch=16,
    optimizer="SGD",
    lr0=0.001,
    lrf=0.01,
    momentum=0.937,
    weight_decay=0.0008,
    warmup_epochs=5,
    cos_lr=True,
    close_mosaic=10,
    label_smoothing=0.05,
    patience=30,
    seed=42,
    deterministic=True,
    workers=0,
    val=False,  # 关闭每 epoch 验证，训练完成后对 best.pt 统一验证
    project=str(ROOT / "runs" / "compare"),
    exist_ok=True,
)

# 完整数据增强策略（两组一致）
AUG = dict(
    mosaic=0.5,
    mixup=0.2,
    hsv_h=0.02,
    hsv_s=0.8,
    hsv_v=0.5,
    degrees=5,
    translate=0.1,
    scale=0.5,
    fliplr=0.5,
    erasing=0.4,
    auto_augment="randaugment",
)


def parse_args():
    parser = argparse.ArgumentParser(description="YOLOv8n vs YOLOv8s 对比实验")
    parser.add_argument("--device", type=str, default="0",
                        help="训练设备，默认 0（GPU）")
    return parser.parse_args()


def train_and_eval(model_name: str, device: str):
    """训练指定模型，返回（参数量/百万, mAP50, mAP50-95）"""
    model_path = str(ROOT / f"{model_name}.pt")
    model = YOLO(model_path)
    model.train(**COMMON, name=model_name, device=device, **AUG)

    best_path = ROOT / "runs" / "compare" / model_name / "weights" / "best.pt"
    best = YOLO(str(best_path))

    # 参数量统计（百万）
    params_m = sum(p.numel() for p in best.model.parameters()) / 1e6

    metrics = best.val(imgsz=COMMON["imgsz"], device=device, verbose=False)
    return params_m, metrics.box.map50, metrics.box.map


def main():
    args = parse_args()

    print("\n===== YOLOv8n vs YOLOv8s 对比实验 =====\n")
    print(f"{'Model':<10}{'Params(M)':<12}{'mAP50':<12}{'mAP50-95':<12}")

    results = {}
    for name in ["yolov8n", "yolov8s"]:
        print(f"\n--- 训练 {name} ---")
        params_m, map50, map5095 = train_and_eval(name, args.device)
        results[name] = (params_m, map50, map5095)
        print(f"{name:<10}{params_m:<12.2f}{map50:<12.4f}{map5095:<12.4f}")

    print("\n===== 对比完成 =====")
    for name, (p, m50, m5095) in results.items():
        print(f"{name}: Params={p:.2f}M, mAP50={m50:.4f}, mAP50-95={m5095:.4f}")


if __name__ == "__main__":
    main()
