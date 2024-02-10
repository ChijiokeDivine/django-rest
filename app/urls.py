from django.urls import path
from . import views
urlpatterns = [
    path('users/', views.UserView.as_view(), name='users'),
    path('customer-login/', views.customer_login, name='customer_login'),
    path('customer-register/', views.CustomerRegisterView.as_view(), name='customer_register'),
    # path('create-user/', views.UserCreateView.as_view(), name='create-user'),
    path('categories', views.CategoryList.as_view()),
    path('products',views.ProductList.as_view()),
    path('product-image', views.ProductImageList.as_view()),
    path('Niches', views.NicheList.as_view()),
    path('Niche/<int:pk>/', views.NicheDetail.as_view()),
    path('cart-order', views.CartOrderList.as_view()),
    path('cart-items', views.CartOrderItemsList.as_view()),
    path('cart-items/increase/<int:pk>/', views.CartOrderItemsIncrease.as_view(), name='cart-increase'),
    path('cart-items/decrease/<int:pk>/', views.CartOrderItemsDecrease.as_view(), name='cart-decrease'),
    path('cart-items/<int:pk>/delete/', views.CartOrderItemDeleteView.as_view(), name='cart-item-delete'),
    path('cart-items/cart-total/',views.CartOrderItemsTotal, name="cart-total"),
    path('reviews', views.ProductReviews.as_view()),
    path('wishlist', views.WishlistDetail.as_view()),
    path('address', views.AddressDetail.as_view()),
]
  