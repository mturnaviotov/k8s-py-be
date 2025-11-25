import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404, JsonResponse
from django.core import serializers
from django.utils import timezone

from .models import Post 
# Create your views here.

@csrf_exempt
def index(request):
    if request.method == "GET":
        posts = Post.objects.all()
        return HttpResponse(serializers.serialize('json', posts ))
    elif request.method == "POST":
        obj = json.loads(request.body.decode('utf-8'))
        post = Post.objects.create(post_text = obj['post_text'], pub_date = timezone.now())
        post.save
        print("{\"level\" : \"info\", \"message\" : \"post created\"}")
        return HttpResponse([post.id])

@csrf_exempt
def detail(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        print("{\"level\" : \"error\", \"message\" : \"post not found\"}")
        return JsonResponse({"level": "error", "message": "not found"}, status=404)

    if request.method == "GET":
        return HttpResponse(serializers.serialize('json', [post]), content_type="application/json")

    elif request.method in ["PATCH", "PUT"]:
        try:
            data = json.loads(request.body)
            post.post_text = data.get('post_text')
            print("{\"level\": \"info\", \"message\": \"post updated\"}")
            post.save()
        except json.JSONDecodeError:
            return JsonResponse({"level": "error", "message": "Invalid JSON"}, status=400)
        return HttpResponse(serializers.serialize('json', [post]), content_type="application/json")

    elif request.method == "DELETE":
        print("{\"level\": \"info\", \"message\": \"post deleted\"}")
        post.delete()
        return HttpResponse(status=204)

    return HttpResponse(status=405) # 405 Method Not Allowed