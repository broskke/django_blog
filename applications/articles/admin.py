from django.contrib import admin
from .models import Article, Tag, Comment, Like, Rating

# Register your models here.
admin.site.register([Article, Tag, Comment, Like, Rating])
