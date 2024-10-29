from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('member_list/', views.member_list, name='member_list'),
    path('add_member/', views.add_member, name='add_member'),
    path('member/<int:member_id>/', views.member_detail, name='member_detail'),
    path('borrow/', views.borrow_item, name='borrow_item'),
    path('return/', views.return_list, name='return_item'),
    path('return/<int:loan_id>/confirm/', views.confirm_return, name='confirm_return'),  # Pour confirmer un retour spécifique
    path('media/<str:media_type>/', views.media_list, name='media_list'),
    path('media/<str:media_type>/add/', views.media_add, name='media_add'),
    path('media/<str:media_type>/<int:item_id>/', views.media_detail, name='media_detail'),
    path('boardgames/', views.boardgame_list, name='boardgame_list'),
    path('boardgame/add/', views.boardgame_add, name='boardgame_add'),
    path('boardgame/<int:boardgame_id>/', views.boardgame_detail, name='boardgame_detail'),
]