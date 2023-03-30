from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Article(models.Model):
    STATUS_CHOICES = (
        ('OPEN','Open'),
        ('CLOSED','Closed'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='articles',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    tag = models.ManyToManyField("Tag", related_name='articles')
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='CLOSED')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['created_at']

    def __str__(self) -> str:
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.title
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sub_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    
    def __str__(self) -> str:
        return f'Комментарий от {self.user.username}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return f'Liked by {self.user.username}'
    

class Rating(models.Model):
    RATES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ratings')
    rate = models.PositiveSmallIntegerField(choices=RATES)
    # rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    def __str__(self):
        return str(self.rate)
    
    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        unique_together = ['user','article']

    


"""
1. Написать модель(models.py)
2. Добавить в админку (admin.py)
3. Сериализовать её (serializers.py - нужно создать)
4. Отобразит во вьюшке (views.py)
5. Добавить пути (urls.py)
"""

