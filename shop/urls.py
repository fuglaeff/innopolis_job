from django.urls import path

from shop import views

app_name = 'shop'

urlpatterns = [

    path('order/', views.OrderView.as_view()),
    path('order/delete/<int:id>/', views.OrderItemView.as_view()),

    path('item/<int:id>/', views.ItemView.as_view()),
    path('buy/', views.BuyView.as_view()),
]
