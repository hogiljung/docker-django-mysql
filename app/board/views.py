import logging

import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, serializers
from rest_framework.decorators import api_view
from rest_framework import status

from sign.models import Users
from board.models import Post, Content, Comment
from board.serializers import PostSerializer, CommentSerializer, UserSerializer, TitleSerializer
from rest_framework.response import Response


# Create your views here.
class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # @csrf_exempt
    # @api_view(('GET',))
    # def briefContentView(request):      #/titleview/
    #     post = Post.objects.all()
    #     serializer = PostSerializer(post, many=True)
    #     return JsonResponse(serializer.data, safe=False)

    @csrf_exempt
    @api_view(('GET',))
    def briefContentView(request):  # /titleview/
        post = Post.objects.exclude(deleted=1).all()
        serializer = TitleSerializer(post, many=True)
        data = dict(
            content=serializer.data,
            code='000'
        )
        # logger = logging.getLogger('test')
        # logger.error(data)
        return JsonResponse(data, safe=False)

    @csrf_exempt
    @api_view(('POST',))
    def contentView(request):  # /contentview/
        print(request.POST)
        post_id = request.POST.get('post_id')
        post = Post.objects.filter(id=post_id).first()
        content = Content.objects.filter(post_id=post_id).first()
        print(content.content)
        d = dict(
            title=post.title,
            content=content.content,
        )
        data = dict(
            content=d,
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
        post = Post.objects.create(title=title, brief_description=brief_description, user_id=Users.objects.filter(id=user).first(), deleted=0, comment_count=0)
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
        postdata = Post.objects.get(id=post_id)
        if (user_id == post.user_id.id or user.username == "suhun"):
            postdata.deleted = 1
            postdata.save()
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
            a = dict(
                title=title,
                content=content,
                updated_date=postdata.updated_date,
            )
            data = dict(
                content=a,
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

    @csrf_exempt
    @api_view(('POST',))
    def commentView(request):
        post_id = request.POST.get('post_id')
        comment = Comment.objects.filter(post_id=post_id).all()
        comment_serializer = CommentSerializer(comment, many=True)
        data = dict(
            comments=comment_serializer.data,
            code='000',
        )
        # logger = logging.getLogger('test')
        # logger.error(data)
        return Response(data=data)

    @csrf_exempt
    @api_view(('POST',))
    def writeCommentView(request):  # /writecommentview/
        post_id = request.POST.get('post_id')
        content = request.POST.get('content', None)
        user = request.POST.get('user_id')
        comment = Comment.objects.create(content=content, post_id=Post.objects.filter(id=post_id).first(),
                                   user_id=Users.objects.filter(id=user).first())
        u = Users.objects.filter(id=user).first()
        count = Comment.objects.filter(post_id=post_id).all()
        post = Post.objects.filter(id=post_id).first()
        post.comment_count=count.count()
        post.save()
        b = dict(
            id=u.id,
            username=u.username,
        )
        a = dict(
            content=comment.content,
            updated_date=comment.updated_date,
            user=b,
        )
        data = dict(
            comment=a,
            code='000',
        )

        return Response(data=data)

class ContentsView(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = PostSerializer

class CommentsView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer