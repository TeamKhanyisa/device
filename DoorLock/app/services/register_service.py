import os
from datetime import datetime
from pathlib import Path
import numpy as np
from sqlalchemy import text
from deepface import DeepFace

from app.config import config
from app.db.db import engine

# step → filename mapping
ANGLE_FILES = {
    1: "anonymous_front.jpg",
    2: "anonymous_up.jpg",
    3: "anonymous_down.jpg",
    4: "anonymous_left.jpg",
    5: "anonymous_right.jpg",
}


def extract_embedding(image_path: str) -> np.ndarray:
    embedding_obj = DeepFace.represent(
        img_path=image_path,
        model_name=config.MODEL_NAME,
        enforce_detection=True,
    )
    return np.array(embedding_obj[0]["embedding"], dtype=np.float32)


def save_to_db(img_path: str, embedding: np.ndarray, step: int) -> None:
    emb_str = ",".join(map(str, embedding.tolist()))
    q = text(
        """
        INSERT INTO face_embeddings (user_id, model_name, img_path, embedding, created_at, step)
        VALUES (:user_id, :model_name, :img_path, :embedding, :created_at, :step)
        """
    )
    with engine.begin() as conn:
        conn.execute(
            q,
            {
                "user_id": "anonymous",
                "model_name": config.MODEL_NAME,
                "img_path": img_path,
                "embedding": emb_str,
                "created_at": datetime.now(),
                "step": step,
            },
        )


def register_face_step(step: int, file_bytes: bytes):
    if step not in ANGLE_FILES:
        return {"success": False, "error": "Invalid step"}

    os.makedirs(config.REGISTER_DIR, exist_ok=True)
    save_filename = ANGLE_FILES[step]
    save_path = os.path.join(config.REGISTER_DIR, save_filename)

    # Replace existing if re-capturing
    if os.path.exists(save_path):
        try:
            os.remove(save_path)
        except Exception:
            pass

    # Save file
    with open(save_path, "wb") as f:
        f.write(file_bytes)

    # Detect face & persist embedding
    try:
        emb = extract_embedding(save_path)
        save_to_db(save_path, emb, step)
        return {
            "success": True,
            "step": step,
            "message": f"{save_filename} saved successfully",
        }
    except Exception as e:
        try:
            if os.path.exists(save_path):
                os.remove(save_path)
        except Exception:
            pass
        print(f"[ERROR] step {step} failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Face detection failed for step {step}",
        }
