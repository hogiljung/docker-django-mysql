from django.db import models

# Create your models here.
class Users(models.Model):
    uuid = models.CharField(primary_key=True, max_length=100)
    id = models.CharField(unique=True, max_length=20)
    pw = models.CharField(max_length=100)

    class Meta:
        managed = False #테이블 자동생성 막기
        db_table = 'users'