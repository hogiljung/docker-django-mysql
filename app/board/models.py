from django.db import models
from sign.models import Users

# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    brief_description = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id', related_name='user')
    class Meta:
        managed = False #테이블 자동생성 막기
        db_table = 'post'


class Content(models.Model):
    post_id = models.ForeignKey(Post, related_name='post', on_delete=models.CASCADE, primary_key=True, db_column='post_id', unique=True)
    content = models.TextField(max_length=100)
    large_content = models.TextField()
    class Meta:
        managed = False #테이블 자동생성 막기
        db_table = 'post_content'
