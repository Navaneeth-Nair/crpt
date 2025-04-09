from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def push(request):
    if request.method == "POST":
        data = json.loads(request.body)
        return JsonResponse({"status": "ok", "message": "Push received", "data": data})
    return JsonResponse({"error": "Invalid method"}, status=405)

@csrf_exempt
def pull(request):
    if request.method == "POST":
        data = json.loads(request.body)
        return JsonResponse({
            "status": "ok",
            "message": "Pull successful",
            "data": {
                "commit": "abc123",
                "branch": "main",
                "blobs": []
            }
        })
    return JsonResponse({"error": "Invalid method"}, status=405)
