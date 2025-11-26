import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404, JsonResponse
from django.utils import timezone

from .models import Post
from .metrics import POST_OPERATIONS_TOTAL

# Create your views here.

@csrf_exempt
def index(request):
    if request.method == "GET":
        data = [post.to_json() for post in Post.objects.all()]
        POST_OPERATIONS_TOTAL.labels(operation_type='read').inc()
        return JsonResponse(data, safe=False)
    elif request.method == "POST":
        obj = json.loads(request.body.decode('utf-8'))
        post = Post.objects.create(post_text = obj['post_text'], pub_date = timezone.now())
        post.save
        print("{\"level\" : \"info\", \"message\" : \"post created\"}")
        POST_OPERATIONS_TOTAL.labels(operation_type='create').inc()
        return JsonResponse(post.to_json())

@csrf_exempt
def detail(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        print("{\"level\" : \"error\", \"message\" : \"post not found\"}")
        POST_OPERATIONS_TOTAL.labels(operation_type='not_found').inc()
        return JsonResponse({"level": "error", "message": "not found"}, status=404)

    if request.method == "GET":
        POST_OPERATIONS_TOTAL.labels(operation_type='read').inc()
        return JsonResponse(post.to_json())

    elif request.method in ["PATCH", "PUT"]:
        POST_OPERATIONS_TOTAL.labels(operation_type='update').inc()
        try:
            data = json.loads(request.body)
            post.post_text = data.get('post_text')
            print("{\"level\": \"info\", \"message\": \"post updated\"}")
            post.save()
        except json.JSONDecodeError:
            return JsonResponse({"level": "error", "message": "Invalid JSON"}, status=400)
        return JsonResponse(post.to_json())

    elif request.method == "DELETE":
        POST_OPERATIONS_TOTAL.labels(operation_type='delete').inc()
        print("{\"level\": \"info\", \"message\": \"post deleted\"}")
        post.delete()
        return HttpResponse(status=204)

    return HttpResponse(status=405) # 405 Method Not Allowed