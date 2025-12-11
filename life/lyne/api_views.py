from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from deepface import DeepFace
from PIL import Image
import numpy as np
import tempfile
import os


def load_image_to_tempfile(django_file):
    """Convert Django upload to a real temp file path for DeepFace"""
    img = Image.open(django_file)
    if img.mode != "RGB":
        img = img.convert("RGB")

    temp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    img.save(temp, format="JPEG")
    temp.flush()
    return temp.name


@csrf_exempt
def verify_face(request):
    if request.method != "POST":
        return JsonResponse({"match": False, "score": 0, "message": "POST required"}, status=405)

    id_file = request.FILES.get("id_proof_front")
    selfie_file = request.FILES.get("selfie")
    uploaded_file = request.FILES.get("uploaded_photo")
    threshold = float(request.POST.get("threshold", 75))

    if not id_file:
        return JsonResponse({"match": False, "score": 0, "message": "Missing ID"}, status=400)

    probe = selfie_file or uploaded_file
    if not probe:
        return JsonResponse({"match": False, "score": 0, "message": "Missing probe image"}, status=400)

    # temp files must be deleted after use
    id_path = probe_path = None

    try:
        # Convert images → temp file paths
        id_path = load_image_to_tempfile(id_file)
        probe_path = load_image_to_tempfile(probe)

        # Run DeepFace verification
        result = DeepFace.verify(
            img1_path=id_path,
            img2_path=probe_path,
            model_name="Facenet512",
            enforce_detection=False,
        )

        distance = result.get("distance")
        if distance is None:
            return JsonResponse({
                "match": False,
                "score": 0,
                "message": "Face not detected or comparison failed"
            })

        # Convert distance → similarity percentage
        score = max(0, (1 - distance)) * 100
        match = score >= threshold

        return JsonResponse({
            "match": match,
            "score": round(score, 2),
            "message": "OK"
        })

    except Exception as e:
        return JsonResponse({
            "match": False,
            "score": 0,
            "message": f"Error: {str(e)}"
        }, status=500)

    finally:
        # ALWAYS clean temp files
        if id_path and os.path.exists(id_path):
            os.remove(id_path)
        if probe_path and os.path.exists(probe_path):
            os.remove(probe_path)