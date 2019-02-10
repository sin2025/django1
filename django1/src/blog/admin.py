from django.contrib import admin
from pip._vendor.urllib3 import filepost

from .models import Post, PostFild, PostImage, PostType

# Register your models here.
admin.site.register(Post)
admin.site.register(PostFild)
admin.site.register(PostImage)
admin.site.register(PostType)
#관리자사이트에서 생성


