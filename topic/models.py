from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 討論主題
class Topic(models.Model):
    subject = models.CharField('討論主題', max_length=255)
    content = models.TextField('內文')
    author = models.ForeignKey(User, on_delete=models.CASCADE) #作者連結到User #CASCADE:當帳號被刪除時，也會將 Topic 這個資料模型裡所有參考到該帳號的紀錄一起刪除。
    created = models.DateTimeField('建立時間', auto_now_add=True) #自動填時間
    replied = models.DateTimeField('回覆時間', null=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.author, self.subject)
#superuser ann password:123456789
