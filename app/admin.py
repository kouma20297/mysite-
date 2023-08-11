from django.contrib import admin
from .models import Post, Category

# モデルの変更をしたらmaigretionをする
admin.site.register(Post)
admin.site.register(Category)