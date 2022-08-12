from django.urls import path
from . import views

urlpatterns = [
    path('',views.IndexView.as_view(),name="home"),
    path('login/', views.User_login.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('adminUsers/create', views.AddAdminUserView.as_view(),name="adminUsersCreate"),
    path('adminUsers/', views.AdminUserListView,name="adminUsersList"),
    path('products/create', views.ProductView.as_view(),name="productCreate"),
    path('products/', views.ProductListView.as_view(),name="productList"),
    path('products/<int:idp>/update', views.ProductUpdateView.as_view(),name="productUpdate"),
    path('products/<int:idp>/delete', views.ProductDeleteView.as_view(),name="productDelete"),
    path('products/<int:idp>/details', views.ProductDetailsView.as_view(),name="productDetails"),
    path('categories/create', views.CategoryView.as_view(),name="categoryCreate"),
    path('categories/', views.CategoryListView.as_view(),name="categoryList"),
    path('orders/', views.OrderListView.as_view(),name="orderlist"),

]


