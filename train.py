from pathlib import Path

from app.service.trainer import Trainer
from app.service.evaluator import Evaluator
from app.service.draw_results import DrawResults
from app.service.draw_model import DrawModel
from app.service.export import Exporter


def main():

    ROOT = Path(__file__).resolve().parent

    DATA = ROOT / "100种中药分类数据集" / "data" / "data.yaml"

    MODEL = ROOT / "yolov8n.pt"

    PROJECT = ROOT / "runs"

    NAME = "Chinese_Herb"

    trainer = Trainer(

        model_path=str(MODEL),

        data_yaml=str(DATA),

        project=str(PROJECT),

        name=NAME

    )

    trainer.train()

    best_weight = PROJECT / NAME / "weights" / "best.pt"

    print("\n==============================")
    print("开始验证模型")
    print("==============================")

    evaluator = Evaluator(str(best_weight))

    evaluator.evaluate()

    print("\n==============================")
    print("开始绘制训练曲线")
    print("==============================")

    drawer = DrawResults(

        PROJECT / NAME

    )

    drawer.draw()

    print("\n==============================")
    print("开始绘制模型结构")
    print("==============================")

    model_drawer = DrawModel(

        str(best_weight)

    )

    model_drawer.draw()

    print("\n==============================")
    print("开始导出ONNX")
    print("==============================")

    exporter = Exporter(

        str(best_weight)

    )

    exporter.export()

    print("\n==============================")
    print("全部完成")
    print("==============================")


if __name__ == "__main__":

    main()