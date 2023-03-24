from rest_framework.routers import  DefaultRouter
from .views import ArticleViewSet, TagViewSet

router = DefaultRouter()
router.register('article',ArticleViewSet,'articles')
router.register('tags', TagViewSet, 'tags')

urlpatterns = router.urls
