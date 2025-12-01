from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie/<str:movie_id>/', views.movie_detail, name='movie_detail'),  # ★ 추가
    path('schedule/<str:movie_id>/', views.movie_schedule, name='movie_schedule'),
    path('reserve/<str:schedule_id>/', views.reserve, name='reserve'),
    path('reservations/<str:member_id>/', views.reservation_list, name='reservation_list'),
    path('cancel/<str:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('foods/', views.food_list, name='food_list'),
    path('order/<str:food_id>/', views.order_food, name='order_food'),
    path('orders/<str:member_id>/', views.order_list, name='order_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]