import os
from deepface import DeepFace
from sqlalchemy import text

from app.config.config import config
from app.db.db import engine

def verify_face(file_bytes: bytes):
    """Compare uploaded face image with registered faces in DB."""
    os.makedirs(config.REGISTER_DIR, exist_ok=True)
    tmp_path = os.path.join(config.REGISTER_DIR, "temp_verify.jpg")
    with open(tmp_path, "wb") as f:
        f.write(file_bytes)

    with engine.begin() as conn:
        rows = conn.execute(text("SELECT img_path FROM face_embeddings")).fetchall()

    best_match = None
    best_distance = 1.0

    for row in rows:
        img_path = row[0]
        try:
            result = DeepFace.verify(
                img1_path=tmp_path,
                img2_path=img_path,
                model_name=config.MODEL_NAME,
                enforce_detection=False,
            )
            if result["distance"] < best_distance:
                best_distance = result["distance"]
                best_match = result["verified"]
        except Exception as e:
            print(f"[WARN] Compare failed for {img_path}: {e}")

    match = bool(best_match and best_distance < 1)

    return {
        "match": match,
        "distance": float(best_distance),
        "message": "Face verified" if match else "No match found",
    }
