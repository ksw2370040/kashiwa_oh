from django.urls import path
from . import views
# URLパターン 逆引きできるように名前 付ける
app_name = 'gameapp'
# URLパターン 登録する変数
urlpatterns = [ 
    # photoアプリへのアクセスはviewsモジュールのIndexView 実行 
    path('', views.IndexView.as_view(), name='index'),
    path('game-detail/<int:pk>',
         views.DetailView.as_view(),
         name='game_detail'
         ),
    path('post/',views.CreateGameView.as_view(), name='post'),
    path('post_done/',views.PostSuccessView.as_view(),name='post_done'),
    path('games/<int:category>',
         views.CategoryView.as_view(),
         name = 'games_cat'
        ),
    path('user-list/<int:user>', 
         views.UserView.as_view(), 
         name = 'user_list' 
         ),
    path('mypage/', views.MypageView.as_view(), 
         name = 'mypage'
         ),
    path('game/<int:pk>/delete/', views.GameDeleteView.as_view(), 
         name = 'game_delete' ),
    path(
        'contact/',
        views.ContactView.as_view(),
        name='contact',
    ),
     path('comment/<int:pk>', views.CreateCommentView.as_view(), name='comments'),

]