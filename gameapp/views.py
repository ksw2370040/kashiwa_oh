from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import GamePostForm,CommentForm
from django.utils.decorators import method_decorator
from django. contrib.auth.decorators import login_required
from .models import GamePost,Comment
from django.views.generic import DetailView
from django.views.generic import DeleteView
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage
from django.views.generic import FormView

class IndexView(ListView):
    template_name ='index.html'
    context_object_name = 'orderby_records'
    queryset = GamePost.objects.order_by('-posted_at')
    paginate_by = 4

@method_decorator(login_required,name='dispatch')
class CreateGameView(CreateView):
    form_class = GamePostForm
    template_name = 'post_game.html'
    success_url = reverse_lazy('gameapp:post_done')
    def form_valid(self, form) :
        postdate = form.save(commit=False)
        postdate.user = self.request.user
        postdate.save()
        return super().form_valid(form)


class PostSuccessView(TemplateView):
    template_name = 'post_success.html'

class CategoryView(ListView):
    template_name = 'category.html'
    paginate_by = 9
    def get_queryset(self):
        category_id = self.kwargs['category']
        categories = GamePost.objects.filter(
            category=category_id).order_by('-posted_at')
        return categories


class UserView(ListView):
    template_name = 'category.html'
    paginate_by = 9
    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = GamePost.objects.filter(
            user=user_id).order_by('-posted_at')
        return user_list
    
class DetailView(DetailView):
    template_name='detail.html'
    model = GamePost

class CreateCommentView(CreateView):
    form_class = CommentForm
    template_name = 'comment.html'
    model = Comment
 
    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(GamePost, pk=post_pk)
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect('gameapp:game_detail', pk=post_pk)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(GamePost, pk=self.kwargs['pk'])
        return context

class MypageView(ListView):
    template_name ='mypage.html'
    paginate_by = 9
    def get_queryset(self):
        queryset = GamePost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        return queryset

class GameDeleteView(DeleteView):
    model=GamePost
    template_name = 'game_delete.html'
    success_url= reverse_lazy('gameapp:mypage')
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
class ContactView(FormView):
    template_name ='contact.html' 
    form_class = ContactForm 
    success_url = reverse_lazy('gameapp:contact') 
    def form_valid(self, form): 
        name = form.cleaned_data['name'] 
        email = form.cleaned_data['email'] 
        title = form.cleaned_data['title'] 
        message = form.cleaned_data['message'] 
        subject = 'お問い合わせ: {}'.format(title) 
        message = \
            '送信者名: {0}\nメールアドレス: {1}\n タイトル:{2}\n メッセージ:\n{3}' \
            .format(name, email, title, message)
        from_email = 'blogapp.2370040@gmail.com'
        to_list = ['blogapp.2370040@gmail.com'] 
        message = EmailMessage(subject=subject, 
                               body=message, 
                               from_email=from_email, 
                               to=to_list, 
                               ) 
        try:
            message.send()
            messages.success(self.request, "送信完了")
        except Exception as e:
            messages.error(self.request, f"送信失敗:{e}")
        return super().form_valid(form)