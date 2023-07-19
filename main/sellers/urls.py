from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns =[
    path('sellerSignUp/', SignUp.as_view(), name='ssignup'),
    path('sellerLogIn/', LogIn.as_view(), name='slogin'),
    path('sellerLogOut/', LogOut.as_view(), name='slogout'),
    path('productdetails/<int:pid>', ProDetail.as_view(), name = 'detail'),
    path('Cart/', CartView.as_view(), name = 'cart'),
    path('like/<int:id>', ProLike.as_view(), name='like'),
    
    path('feedLike/<int:id>', feedLike, name='feedlike'),
    path('feedEdit/<int:id>', FeedEdit.as_view(), name='feededit'),
    path('feedRemove/<int:id>', feedRemove, name='feedremove'),
]