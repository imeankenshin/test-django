import imp
import django
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from blog.models import Article

class AccountLoginView(LoginView):
    """ログインページのテンプレート"""
    template_name = 'blog/login.html'

    def get_default_redirect_url(self):
        """ログインに成功した時に飛ばされるURL"""
        return "/blog"
class AccountCreateView(View):
    def get(self, request):
        return render(request, "blog/register.html")
    
    # post を追加
    def post(self, request):
        # ユーザー情報を保存する
        User.objects.create_user(
            username=request.POST["username"],
            password=request.POST["password"],
        )
        # 登録完了画面を表示する
        return render(request, "blog/register_success.html")
def index():
    return HttpResponse("Hello, world.")
def detail():
    return HttpResponse("detail page")
def index(request):
    return render(request, "blog/index.html")

class MypageView(LoginRequiredMixin, View):
    login_url= "blog/login.html"
    
    def get(self, request):
        return render(request, "blog/mypage.html")
    
class AccountLogoutView(LogoutView):
    template_name = 'blog/logout.html'
    
class ArticleCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "blog/article_new.html")

class MypageArticleView(LoginRequiredMixin, View):
    def post(self, request):
        """新しく記事を作製する"""
        # リクエストで受け取った情報をDBに保存する
        article = Article(
            title=request.POST["title"],
            body=request.POST["body"],
            # user には、現在ログイン中のユーザーをセットする
            user=request.user,
        )
        article.save()
        return render(request, "blog/article_created.html")

class ArticleListView(View):
    def get(self, request):
        # Django の機能である model を使ってすべての記事を取得する
        # articles は Article のリストになる
        articles = Article.objects.all()
        
        # 取得した記事一覧をテンプレートにわたす
        # こうすると、テンプレートの中で articles という変数が渡せる
        return render(request, "blog/articles.html", {
            "articles": articles
        })