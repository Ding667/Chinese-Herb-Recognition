# 基于 YOLOv8n 的中草药识别系统

基于轻量化目标检测算法 YOLOv8n 的中草药图像识别系统，支持 **100 类中草药**的自动检测与分类。用户上传药材图像后，系统自动检测目标、返回类别名称与置信度并绘制检测框，同时通过 MySQL 保存识别历史，支持历史查询与删除。系统面向药房入库验收、药材市场抽检、中药教学科普等场景。

## 功能特性

- **图像识别**：上传图片，YOLOv8n 检测并分类 100 类中草药，输出类别、置信度与位置信息
- **用户系统**：注册 / 登录（密码 sha256 + 随机盐存储，不落明文）
- **历史记录**：识别记录持久化到 MySQL，支持查询与删除
- **可视化**：检测框绘制、模型指标看板、训练曲线展示
- **模型工具链**：训练、评估、导出、结构可视化等完整脚本

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Vue3 + Vite + Element Plus + ECharts |
| 后端 | FastAPI + Uvicorn + PyMySQL |
| 算法 | YOLOv8n（Ultralytics） |
| 数据库 | MySQL 8.0 |
| 训练环境 | RTX 5060 Laptop / CUDA 13.1 / PyTorch 2.11.0 / Ultralytics 8.4.75 |

## 模型性能（最终模型 A1：YOLOv8n + Mosaic + MixUp）

- 数据集：100 类中草药，训练集 7518 张 / 验证集 1767 张
- **mAP@0.5 = 0.8750**，**mAP@0.5:0.95 = 0.8729**
- Precision = 0.8364，Recall = 0.8253
- Top-1 准确率 82.57%，Top-5 准确率 87.32%
- 推理速度 66.48 FPS，参数量 3.35M，计算量 14.0 GFLOPs

## 项目结构

```
├── app/                      # 后端应用（FastAPI）
│   ├── main.py               # 入口：路由注册、CORS、静态挂载、数据库初始化
│   ├── config.py             # MySQL 连接配置
│   ├── db.py                 # 历史记录与用户存储
│   ├── security.py           # 密码哈希（sha256 + salt）
│   ├── api/
│   │   ├── auth.py           # 注册 / 登录接口
│   │   └── detect.py         # 检测、历史记录、类别、健康检查接口
│   └── service/              # 业务模块
│       ├── predictor.py      # 模型推理
│       ├── trainer.py        # 模型训练
│       ├── evaluator.py      # 模型评估
│       ├── export.py         # 模型导出
│       ├── draw_results.py   # 训练曲线绘制
│       └── draw_model.py     # 模型结构导出
├── frontend/                 # 前端应用（Vue3 + Vite）
│   └── src/
│       ├── views/            # 识别 / 历史 / 模型信息 / 登录 / 注册 / 仪表盘
│       ├── components/       # 指标卡 / 结果卡 / 侧边栏 / 上传卡
│       ├── router/           # 前端路由
│       └── api/              # 后端请求封装
├── weights/                  # 训练好的模型权重（best_A1.pt 为最终模型）
├── experiments/              # 消融与对比实验脚本
├── tools/                    # 模型结构可视化 / 测速脚本
├── train.py                  # 训练脚本
└── Accuracy.py               # Top-1/Top-5 准确率统计
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

> 训练需 CUDA 版 PyTorch，请根据 GPU 型号从 PyTorch 官网安装对应版本。

### 2. 配置数据库

编辑 `app/config.py`，填写 MySQL 连接信息（程序启动时会自动创建数据库 `herb_recognition` 与数据表）。

### 3. 启动后端

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

接口文档（Swagger）：`http://127.0.0.1:8000/docs`

### 4. 启动前端

```bash
cd frontend
npm install
npm run dev
```

## API 接口说明

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/register` | 用户注册 |
| POST | `/api/login` | 用户登录 |
| POST | `/api/detect` | 上传图像执行检测（multipart/form-data，字段名 `file`） |
| GET | `/api/history` | 查询识别历史（按时间倒序） |
| DELETE | `/api/history/{id}` | 删除指定历史记录 |
| GET | `/api/classes` | 获取类别列表 |
| GET | `/api/health` | 健康检查（返回运行状态与当前模型） |

检测响应示例：

```json
{
  "code": 200,
  "message": "检测成功",
  "data": {
    "image": "/results/xxx.jpg",
    "count": 2,
    "results": [
      {"class_id": 0, "class_name": "安息香", "confidence": 0.77, "bbox": [0, 0, 500, 500]}
    ]
  }
}
```

## 数据集说明

本项目使用 100 类中草药图像数据集（训练集 7518 张 / 验证集 1767 张）。数据集体积较大，未纳入本仓库，如需复现请联系作者获取。

## License

本项目仅用于学习与毕业设计展示，数据集版权归原数据源所有。
