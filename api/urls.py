from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from rest_framework.routers import DefaultRouter

#modelviewsetを継承してきたものは、routerを使ってurlとviewの連携を行う
#routerを作る
router = DefaultRouter()
#registerを使うことで、modelsviewsetのviewとurlを連携させることができる
router.register('segments', views.SegmentViewSet)
router.register('brands', views.BrandViewSet)
router.register('vehicles', views.VehicleViewSet)

#app_nameにapiという名前をつける
app_name = 'api'

#genericから継承したviewはurlpatternsでurlとviewを連携させる
urlpatterns = [
    path('create', views.CreateUserView.as_view(), name='create'),
    path('profile/', views.ProfileUserView.as_view(), name='profile'),
    #tokenを返すエンドポイントとしてauth/を追加
    #authのエンドポイントに対して、usernameとpasswordでPOSTメソッドでアクセスしたときに、tokenを返すエンドポイント
    #django-rest-frameowrkに標準装備されているobtain_auth_tokenに紐付けることで実装できる
    path('auth/', obtain_auth_token, name='auth'),
    #ルートのurlにアクセスがあった場合はrouter.registerのurlにアクセスさせる
    path('', include(router.urls)),
]
