"""
=========================================================
FastAPI 主程序
项目：基于轻量化图像检测算法的中草药识别系统
=========================================================
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse

from app.api.detect import router as detect_router
from app.api.auth import router as auth_router
from app.db import init_db


# =====================================================
# 创建FastAPI对象
# =====================================================

app = FastAPI(

    title="中草药识别系统",

    description="基于YOLOv8的中草药智能识别",

    version="1.0.0"

)


# =====================================================
# 跨域
# =====================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


# =====================================================
# 根目录
# =====================================================

ROOT = Path(__file__).resolve().parent.parent


# =====================================================
# 创建目录
# =====================================================

(ROOT / "uploads").mkdir(exist_ok=True)

(ROOT / "results").mkdir(exist_ok=True)

(ROOT / "static").mkdir(exist_ok=True)

try:
    init_db()
except Exception as e:
    print("数据库初始化失败，历史记录功能不可用：", e)


# =====================================================
# 静态资源
# =====================================================

app.mount(

    "/static",

    StaticFiles(directory=ROOT / "static"),

    name="static"

)

app.mount(

    "/uploads",

    StaticFiles(directory=ROOT / "uploads"),

    name="uploads"

)

app.mount(

    "/results",

    StaticFiles(directory=ROOT / "results"),

    name="results"

)


# =====================================================
# 注册接口
# =====================================================

app.include_router(

    detect_router,

    prefix="/api",

    tags=["中草药识别"]

)

app.include_router(

    auth_router,

    prefix="/api",

    tags=["用户"]

)


# =====================================================
# 页面路由
# =====================================================

@app.get("/detect", response_class=HTMLResponse)
async def detect_page():
    return FileResponse(ROOT / "templates" / "detect.html")


@app.get("/history", response_class=HTMLResponse)
async def history_page():
    return FileResponse(ROOT / "templates" / "history.html")


# =====================================================
# 首页
# =====================================================

@app.get("/", response_class=HTMLResponse)

async def index():

    return """

    <html>

    <head>

    <title>中草药识别系统</title>

    </head>

    <body style="font-family:微软雅黑">

        <h1>🌿 中草药识别系统</h1>

        <hr>

        <p>系统运行成功！</p>

        <p><a href="/detect">图片识别</a> | <a href="/history">历史记录</a></p>

        <p>

        Swagger：

        <a href="/docs">

        /docs

        </a>

        </p>

        <p>

        ReDoc：

        <a href="/redoc">

        /redoc

        </a>

        </p>

    </body>

    </html>

    """


# =====================================================
# 启动
# =====================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "app.main:app",

        host="0.0.0.0",

        port=8000,

        reload=True

    )