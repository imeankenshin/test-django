import imp
import django
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from blog.models import Article
from blog.quitta import QiitaApiClient
from django.http import JsonResponse
import json

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

def detail():
    return HttpResponse("detail page")

def index(request):
    # Article の model を使ってすべての記事を取得する
    # Article.objects.all() は article のリストが返ってくる
    articles = Article.objects.all()

    #QuittaのAPIを読み込む
    qitta_api = QiitaApiClient()
    
    # qiita の API がエラーになったかどうか表すフラグ
    is_qiita_error = False
    # 記事一覧を初期化しておく
    qitta_articles = []
    
    try:
        qitta_articles = qitta_api.get_django_articles()
    except RuntimeError:
        is_qiita_error = True
    
    # こうすることで、article 変数をテンプレートにわたす事ができる
    # {テンプレート上での変数名: 渡す変数}
    print(qitta_articles)
    return render(request, "blog/index.html", {
        "articles": articles,
        "qiita_articles": qitta_articles,
    })

class MypageView(LoginRequiredMixin, View):
    login_url= "blog/login.html"
    
    def get(self, request):
        articles = Article.objects.filter(user=request.user)
        return render(request, "blog/mypage.html", {
            "articles": articles
        })
    
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

class ArticleView(View):
    def get(self, request, id):
        article = Article.objects.get(id=id)
        return render(request,"blog/article.html", {
            "article":article
        })
        
class ArticleApiView(View):
    def get(self, req):
        #DBからArticleを取得
        articles = Article.objects.all()
        
        dict_articles = []
        for article in articles:
            dict_article = {
                "id":article.id,
                "title": article.title,
                "body": article.body,
            }
            dict_articles.append(dict_article)
            
        json = {
            "articles": dict_article,
        }
        return JsonResponse(json)
    
    #TODO: 記事を投稿するAPIを作る。 Cookie = csrftoken=bQN8DCuGVhyo1l9ghxNSChikNcTstEKE; Sessionid=9uiippo8ltmb93bvq1noqr80flu6o45e;
    def post(self,request):
        json_dict = json.loads(request.body)
        article = Article(
            title=json_dict["title"],
            body=json_dict["body"],
            # user には、現在ログイン中のユーザーをセットする
            user=request.user,
        )
        article.save()
        return JsonResponse({
            "message": "記事の投稿に成功しました。"
        })