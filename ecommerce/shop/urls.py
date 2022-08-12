from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.IndexView.as_view(),name="home"),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.User_login.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('rechercher/', views.rechercher, name='rechercher'),
    path('products/', views.ProductListView.as_view(),name="productList"),
    path('products/<int:idp>/details', views.ProductDetailsView.as_view(),name="productDetails"),
    path('caregories/<int:idc>/products/', views.ProductsByCategoryView.as_view(),name="productByCetgorie"),
    path('cart/', views.cart_detail,name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove,name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('create/', views.order_create, name='order_create'),
    path('profile/',views.ProfileView.as_view(),name="profile"),
    path('profile/<int:idp>/update', views.ProfileUpdateView.as_view(),name="profileupdate"),
    path('myorders/',views.MyordersView.as_view(),name="orders"),
    path('myorders/<int:ido>/payment/',views.PaymentView.as_view(),name="payment"),    

]


