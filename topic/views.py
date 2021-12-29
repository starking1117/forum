#怎麼收集資料
from django.views.generic import *
from django.urls import reverse
from .models import *
from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin

# 討論主題列表
class TopicList(ListView):
    model = Topic
    ordering = ['-created']
    paginate_by = 20        # 每頁主題數 #分頁

# 新增討論主題
class TopicNew(LoginRequiredMixin,CreateView):
    model = Topic
    fields = ['subject', 'content'] #一定要有

    def get_success_url(self): #新增完主題回到列表
        return reverse('topic_list') #name反推

    def form_valid(self, form): #表單驗證認證
        # 自動將目前使用者填入討論主題的作者欄
        form.instance.author = self.request.user #instance=Topic
        return super().form_valid(form)

# 檢視討論主題
class TopicView(DetailView):
    model = Topic

    def get_context_data(self, **kwargs):
        # 取得回覆資料傳給頁面範本處理
        ctx = super().get_context_data(**kwargs)
        ctx['reply_list'] = Reply.objects.filter(topic=self.object)
        return ctx

    def get_object(self):
        topic = super().get_object()    # 取得欲查看的討論主題
        topic.hits += 1     # 等同 topic.hits = topic.hits + 1
        topic.save()
        return topic

# 回覆討論主題
class TopicReply(LoginRequiredMixin,CreateView):
    model = Reply
    fields = ['content']
    template_name = 'topic/topic_form.html'

    def form_valid(self, form): #缺的欄位在這時候填
        topic = Topic.objects.get(id=self.kwargs['tid'])
        form.instance.topic = topic #年少輕狂
        #form.instance.topic_id = self.kwargs['tid']
        form.instance.author = self.request.user
        topic.replied = datetime.now()  # 更新討論主題回覆時間
        topic.save() #自己填資料要自己存檔 (datetime)
        return super().form_valid(form) #叫TopicReply/CreateView驗證

    def get_success_url(self):
        return reverse('topic_view', args=[self.kwargs['tid']]) #id會變動利用args告訴他

# 刪除討論主題
class TopicDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'topic.delete_topic' #view,add,change,delete
    model = Topic
    template_name = 'confirm_delete.html'
    pk_url_kwarg = 'tid'

    def get_success_url(self):
        return reverse('topic_list')