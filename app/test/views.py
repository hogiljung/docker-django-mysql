import logging

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from .models import Users
from rest_framework import viewsets, status
from .serializers import PostSerializer
"""
class UserView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = PostSerializer
"""

class TestView(APIView):
    queryset = Users.objects.all()
    serializer_class = PostSerializer

    @csrf_exempt
    @api_view(('POST',))
    def signin(request):
        id = request.POST.get('id', None)
        pw = request.POST.get('pw', None)
        user = Users.objects.filter(id=id).first()
        if user is None:
            data = dict(
                msg='id 불일치',
                code='001'
            )
            return Response(data)
        if check_password(pw, user.pw):
            data = dict(
                msg='로그인 성공',
                code='000'
            )
            return Response(data=data)
        else:
            data = dict(
                msg='패스워드 불일치',
                code='002'
            )
            return Response(data=data)

    @csrf_exempt
    @api_view(('POST',))
    def signup(request):
        if request.method == 'POST':
            uuid = request.POST.get('uuid', None)
            id = request.POST.get('id', None)
            pw = request.POST.get('pw', None)
            pw_crypted = make_password(pw)

            if Users.objects.filter(id=id).exists():
                data = dict(
                    msg='이미 존재하는 아이디 입니다.',
                    code='001'
                )
                return Response(data=data)
            else:
                logger = logging.getLogger('test')
                logger.error(uuid)
                logger.error(id)
                logger.error(pw)
                Users.objects.create(uuid=uuid, id=id, pw=pw_crypted)
                user = dict(
                    uuid=uuid,
                    id=id,
                    pw=pw_crypted,)
                data = dict(
                    user = user,
                    msg='회원가입 성공',
                    code='0000'
                )
                return Response(data=data)


        """
            id = request.POST.get('id', None)
            pw = request.POST.get('pw', None)
            user = Users.objects.filter(id=id).first()

            if user is None:
                data = dict(
                    msg='id 불일치',
                    code='001'
                )
                return Response(data)
            if check_password(pw, user.pw):
                data = dict(
                    msg='로그인 성공',
                    code='000'
                )
                return Response(data=data)
            else:
                data = dict(
                    msg='패스워드 불일치',
                    code='002'
                )
                return Response(data=data)
"""