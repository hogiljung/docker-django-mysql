import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import status

from sign.models import Users
from board.models import Post, Content
from board.serializers import PostSerializer, UserSerializer
from rest_framework.response import Response


# Create your views here.
class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @csrf_exempt
    @api_view(('GET',))
    def briefContentView(request):      #/titleview/
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return JsonResponse(serializer.data, safe=False)

    @csrf_exempt
    @api_view(('POST',))
    def contentView(request):  # /contentview/
        post_id = request.POST.get('post_id')
        content = Content.objects.filter(post_id=post_id).first()
        print(content.content)
        c = dict(
            content=content.content
        )
        data = dict(
            content=c,
            code='000'
        )
        return Response(data=data)
    @csrf_exempt
    @api_view(('POST',))
    def postContentView(request):   #/post/
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        user = request.POST.get('user_id')
        if(len(content)>7):
            brief_description = str(content)[0:7] + "..."
        else:
            brief_description = content
        post = Post.objects.create(title=title, brief_description=brief_description, user_id=Users.objects.filter(id=user).first())
        Content.objects.create(post_id=Post.objects.filter(id=post.id).first(), content=content,)
        data = dict(
            #msg='글작성 성공',
            code='000'
        )
        return Response(data=data)

    @csrf_exempt
    @api_view(('POST',))
    def deleteContentView(request):     #/delete/
        post_id = request.POST.get('post_id')
        user_id = request.POST.get('user_id')
        post = Post.objects.filter(id=post_id).first()
        user = Users.objects.filter(id=user_id).first()
        if (user_id == post.user_id.id or user.username == "suhun"):
            post.delete()
            data = dict(
                #msg='글 삭제 완료',
                code='000'
            )
        else:
            data = dict(
                #msg='작가 불일치',
                code='001'
            )
        return Response(data=data)

    @csrf_exempt
    @api_view(('POST',))
    def modifyContentView(request):     #/modify/
        post_id = request.POST.get('post_id')
        user_id = request.POST.get('user_id')
        post = Post.objects.filter(id=post_id).first()
        user = Users.objects.filter(id=user_id).first()
        if (user_id == post.user_id.id or user.username == "suhun"):
            postdata = Post.objects.get(id=post_id)
            contentdata = Content.objects.get(post_id=post_id)
            title = request.POST.get('title', None)
            content = request.POST.get('content', None)
            if (len(content) > 7):
                brief_description = str(content)[0:7] + "..."
            else:
                brief_description = content
            postdata.title = title
            postdata.brief_description = brief_description
            contentdata.content = content
            contentdata.save()
            postdata.save()
            data = dict(
                #msg='글 수정 완료',
                code='000'
            )
        else:
            data = dict(
                #msg='작가 불일치',
                code='001'
            )
        return Response(data=data)

    @csrf_exempt
    @api_view(('POST',))
    def checkAuthorView(request):   #/checkauthorview/
        post_id = request.POST.get('post_id')
        user_id = request.POST.get('user_id')
        post = Post.objects.filter(id=post_id).first()
        user = Users.objects.filter(id=user_id).first()

        if (user_id == post.user_id.id or user.username == "suhun"):
            data = dict(
                msg='작가 일치',
                code='000'
            )
        else:
            data = dict(
                msg='작가 불일치',
                code='001'
            )
        return Response(data=data)

class ContentsView(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = PostSerializer
