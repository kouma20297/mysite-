from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    name = models.CharField('カテゴリ', max_length=100)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.PROTECT)
    title = models.CharField("タイトル", max_length = 200)
    content = models.TextField("本文")
    created = models.DateTimeField("作成日", default=timezone.now)
    
    def __str__(self):
        return self.title
    
    


    
    
# ForeignKey..ほかのモデルと連携できる (ログインユーザーを連携している
# on_delete..は連携先が削除されたら一緒に削除されるようにするもの
# CharField..max_lengthを指定しないといけない
 