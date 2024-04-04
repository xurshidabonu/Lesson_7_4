from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from app_news.models import News
from django.views.generic import FormView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import MurojatForm


# Create your views here.
class AddNewsView(LoginRequiredMixin, CreateView):
    template_name = 'news/add_news.html'
    model = News
    success_url = reverse_lazy('home')
    fields = ['news_title', 'news_description', 'news_image', 'news_content', 'news_category']

    def form_valid(self, form):
        form.instance.news_author = self.request.user
        return super().form_valid(form)


class ListNewsView(ListView):
    template_name = 'news/list_news.html'
    model = News
    paginate_by = 2
    # context_object_name = 'xabar'


class DetailNewsView(DetailView):
    template_name = 'news/show_news.html'
    model = News


class UpdateNewsView(LoginRequiredMixin, UpdateView):
    template_name = 'news/update_news.html'
    model = News
    success_url = reverse_lazy('home')
    fields = ['news_title', 'news_description', 'news_image', 'news_content', 'news_category']

    def form_valid(self, form):
        form.instance.news_author = self.request.user
        return super().form_valid(form)


class DeleteNewsView(LoginRequiredMixin, DeleteView):
    template_name = 'news/delete_news.html'
    model = News
    success_url = reverse_lazy('home')


class SuperuserMurojatView(UserPassesTestMixin, FormView):
    template_name = 'news/form.html'
    form_class = MurojatForm
    success_url = 'home'

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        users = User.objects.filter(is_superuser=False)
        for user in users:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
        return super().form_valid(form)
