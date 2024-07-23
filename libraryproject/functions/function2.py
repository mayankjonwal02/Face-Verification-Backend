from deepface import DeepFace
from django.conf import settings


def recognize_face(temp_image_path):
    recogntion = DeepFace.find(
                        img_path=temp_image_path, 
                        db_path=settings.MEDIA_ROOT, 
                        model_name="Facenet", 
                        detector_backend = "retinaface",
                        distance_metric="cosine", 
                        enforce_detection=True
                        )
    return recogntion