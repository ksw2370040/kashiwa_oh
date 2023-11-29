from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from stdimage.models import StdImageField

class Category(models.Model):
    title = models.CharField(
        verbose_name='カテゴリ',
        max_length=20)
    def __str__(self):
        return self.title
    
class GamePost(models.Model):
    user=models.ForeignKey(
        CustomUser,
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリ',
        on_delete=models.PROTECT
    )
    title = models.CharField(
        verbose_name='タイトル',
        max_length=200
    )
    contents = models.TextField(
        verbose_name='攻略情報',
    )
    image1 = models.ImageField(
        verbose_name='イメージ１',
        upload_to = 'photos',
        blank=True,
        null=True
    )
    image2 = models.ImageField(
        verbose_name='イメージ２',
        upload_to = 'photos',
        blank=True,
        null=True
    )
    posted_at = models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True
    )
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    from  .models import GamePost
    user = models.CharField('名前', max_length=255, default='名無し')
    text = models.TextField('コメント')
    created_at = models.DateTimeField(
        '作成日',
        default=timezone.now
    )
    post = models.ForeignKey(
        GamePost,
        on_delete=models.CASCADE,
        verbose_name='対象記事'
    )
    def __str__(self):
        return f'{self.user.username}のコメント - {self.post.title}'

