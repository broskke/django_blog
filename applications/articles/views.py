from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters
from .models import Article, Tag
from .serializers import ArticleListSerializer, ArticleSerializer, TagSerializer
from .permissions import IsAuthor

'''
@api_view - вьюшки на функции

rest_framework.views.APIView - вьюшки на классах без функционала

rest_framework.generics - вьюшки на готовых классах

rest_framework.viewsets - класс для обработки всех операция CRUD
''' 

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter]
    filterset_fields =['tag','status']
    search_fields = ['title','tag__title']
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update','delete']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request':self.request})
        return context

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return super().get_serializer_class()
""" 
actions - действия пользователя:
    list
    retrieve
    create
    update
    delete
"""


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # pagination_class = 