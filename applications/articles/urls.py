from rest_framework.routers import  DefaultRouter
from .views import ArticleViewSet, TagViewSet, CommentViewSet

router = DefaultRouter()
router.register('article',ArticleViewSet,'articles')
router.register('tags', TagViewSet, 'tags')
router.register('comment', CommentViewSet, 'comments')

urlpatterns = router.urls
