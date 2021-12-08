#怎麼收集資料
from django.views.generic import *
from django.urls import reverse
from .models import *

# 討論主題列表
class TopicList(ListView):
    model = Topic
    ordering = ['-created']
    paginate_by = 20        # 每頁主題數 #分頁

# 新增討論主題
class TopicNew(CreateView):
    model = Topic
    fields = ['subject', 'content'] #一定要有

    def get_success_url(self): #新增完主題回到列表
        return reverse('topic_list') #name反推

    def form_valid(self, form): #表單驗證認證
        # 自動將目前使用者填入討論主題的作者欄
        form.instance.author = self.request.user #instance=Topic
        return super().form_valid(form)

# 檢視討論主題
class TopicView(DetailView): #一筆紀錄
    model = Topic
