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
    path('return/', views.return_list, name='return_item'),  # Vue de la liste des retours
    path('return/<int:loan_id>/confirm/', views.confirm_return, name='confirm_return'),  # Pour confirmer un retour spécifique
]