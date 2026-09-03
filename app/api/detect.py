# -*- coding: utf-8 -*-
"""中草药识别接口"""
import json
import uuid
import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from app.service.predictor import Predictor
from app.db import save_history, list_history, delete_history


router = APIRouter()

ROOT = Path(__file__).resolve().parents[2]
UPLOAD_DIR = ROOT / "uploads"
RESULT_DIR = ROOT / "results"
WEIGHT_PATH = ROOT / "weights" / "best.pt"

UPLOAD_DIR.mkdir(exist_ok=True)
RESULT_DIR.mkdir(exist_ok=True)

predictor = Predictor(str(WEIGHT_PATH))


@router.post("/detect")
async def detect(file: UploadFile = File(...)):
    try:
        suffix = Path(file.filename).suffix
        filename = f"{uuid.uuid4().hex}{suffix}"
        upload_path = UPLOAD_DIR / filename
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = predictor.predict(str(upload_path))
        result_path = RESULT_DIR / filename
        predictor.predict_and_save(str(upload_path), str(result_path))

        # 历史记录写入失败不影响识别主流程
        try:
            save_history(
                image_name=filename,
                result_image=filename,
                target_count=result["count"],
                result_json=json.dumps(result["results"], ensure_ascii=False),
            )
        except Exception as e:
            print("历史记录写入失败：", e)

        return JSONResponse(
            {
                "code": 200,
                "message": "检测成功",
                "data": {
                    "image": f"/results/{filename}",
                    "count": result["count"],
                    "results": result["results"],
                },
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def history():
    try:
        records = list_history()
        return {"code": 200, "message": "查询成功", "data": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/history/{record_id}")
async def remove_history(record_id: int):
    try:
        delete_history(record_id)
        return {"code": 200, "message": "删除成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/classes")
async def classes():
    return {"count": predictor.class_count(), "classes": predictor.get_classes()}


@router.get("/health")
async def health():
    return {"status": "running", "model": WEIGHT_PATH.name}
