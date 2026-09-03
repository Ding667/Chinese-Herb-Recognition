# -*- coding: utf-8 -*-
"""模型推理速度测试脚本
用于论文中的推理性能测试，统计单张平均延迟与吞吐量（FPS）。
在 GPU 环境下运行可得到论文所需的真实推理性能数据。
"""
import argparse
import time
from pathlib import Path

import torch
from ultralytics import YOLO

# 项目根目录（tools/ 的上一级）
ROOT = Path(__file__).resolve().parent.parent


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="模型推理速度测试")
    parser.add_argument(
        "--weights", type=str,
        default=str(ROOT / "weights" / "best.pt"),
        help="模型权重路径，默认 weights/best.pt",
    )
    parser.add_argument(
        "--source", type=str,
        default=str(ROOT / "100种中药分类数据集" / "data" / "val" / "images"),
        help="测试图片目录，默认验证集图片目录",
    )
    parser.add_argument(
        "--device", type=str, default="0",
        help="推理设备，默认 0（GPU）",
    )
    return parser.parse_args()


def collect_images(source: Path):
    """收集目录下所有图片路径"""
    exts = {".jpg", ".png", ".jpeg", ".bmp"}
    return [p for p in source.iterdir() if p.suffix.lower() in exts]


def main():
    args = parse_args()

    weights = Path(args.weights)
    source = Path(args.source)

    # 路径检查
    if not weights.exists():
        raise FileNotFoundError(f"模型不存在：{weights}")
    if not source.exists():
        raise FileNotFoundError(f"图片目录不存在：{source}")

    # 加载模型
    model = YOLO(str(weights))

    # 设备检测：指定 GPU 但 CUDA 不可用时回退到 CPU
    device = args.device
    if device in ("cpu", "-1") or not torch.cuda.is_available():
        device = "cpu"
        device_name = "CPU"
    else:
        device_name = torch.cuda.get_device_name(int(device))

    images = collect_images(source)
    if not images:
        raise RuntimeError(f"目录下无图片：{source}")

    # warmup：排除首次推理的模型初始化开销
    model.predict(str(images[0]), device=device, verbose=False, imgsz=640)

    # 正式计时
    start = time.perf_counter()
    for img in images:
        model.predict(str(img), device=device, verbose=False, imgsz=640)
    total_time = time.perf_counter() - start

    n = len(images)
    avg_latency = total_time / n * 1000  # 单张平均延迟（毫秒）
    fps = n / total_time  # 吞吐量（帧/秒）

    # 组装输出
    lines = [
        "====================",
        "Inference Speed Test",
        "====================",
        f"Model:   {weights}",
        f"Device:  {device_name} ({device})",
        f"Images:  {n}",
        "",
        f"Total Time:      {total_time:.2f} s",
        f"Average Latency: {avg_latency:.2f} ms",
        f"FPS:             {fps:.2f}",
    ]
    result = "\n".join(lines)

    print(result)

    # 保存结果到 results/speed_test.txt
    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "speed_test.txt"
    out_file.write_text(result + "\n", encoding="utf-8")
    print(f"\n结果已保存：{out_file}")


if __name__ == "__main__":
    main()
