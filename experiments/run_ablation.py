# -*- coding: utf-8 -*-
"""消融实验训练脚本
读取 ablation_config.yaml，按 --exp 参数运行 A0/A1/A2 三组消融实验。
训练结果保存到 runs/ablation/{A0,A1,A2}，不覆盖 weights/best.pt。
"""
import argparse
from pathlib import Path

import yaml
from ultralytics import YOLO

# 项目根目录（experiments/ 的上一级）
ROOT = Path(__file__).resolve().parent.parent


def parse_args():
    parser = argparse.ArgumentParser(description="消融实验训练")
    parser.add_argument(
        "--exp", type=str, required=True, choices=["A0", "A1", "A2"],
        help="实验编号：A0 / A1 / A2",
    )
    return parser.parse_args()


def load_config():
    """读取消融实验配置文件"""
    cfg_file = ROOT / "experiments" / "ablation_config.yaml"
    with open(cfg_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    args = parse_args()
    config = load_config()
    common = config["common"]
    exp = config["experiments"][args.exp]

    # 拼接统一训练参数 + 对应实验的增强参数
    data = str(ROOT / common["data"])
    model_path = str(ROOT / common["model"])

    train_args = dict(
        data=data,
        epochs=common["epochs"],
        imgsz=common["imgsz"],
        batch=common["batch"],
        optimizer=common["optimizer"],
        lr0=common["lr0"],
        lrf=common["lrf"],
        momentum=common["momentum"],
        weight_decay=common["weight_decay"],
        warmup_epochs=common["warmup_epochs"],
        cos_lr=common["cos_lr"],
        close_mosaic=common["close_mosaic"],
        label_smoothing=common["label_smoothing"],
        patience=common["patience"],
        seed=common["seed"],
        deterministic=common["deterministic"],
        workers=common["workers"],
        device=common["device"],
        val=False,  # 关闭每 epoch 验证，训练完成后对 best.pt 统一验证
        project=str(ROOT / "runs" / "ablation"),
        name=args.exp,
        exist_ok=True,
    )
    train_args.update(exp["aug"])

    print(f"\n===== 消融实验 {args.exp}：{exp['description']} =====")

    model = YOLO(model_path)
    model.train(**train_args)

    # 训练完成后统计验证集指标
    best_path = ROOT / "runs" / "ablation" / args.exp / "weights" / "best.pt"
    best = YOLO(str(best_path))
    metrics = best.val(imgsz=common["imgsz"], device=common["device"], verbose=False)

    print("\n===== 训练完成 =====")
    print(f"best.pt 路径: {best_path}")
    print(f"mAP50:        {metrics.box.map50:.4f}")
    print(f"mAP50-95:     {metrics.box.map:.4f}")


if __name__ == "__main__":
    main()
