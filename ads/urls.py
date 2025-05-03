from django.urls import path
from .views import (index, register, home_redirect, create_ad, logout_view, edit_ad, delete_ad, my_ads, create_proposal,
                    all_proposals, update_proposal_status)
from django.contrib.auth import views

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', index, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_redirect, name='home'),
    path('create/', create_ad, name='create_ad'),
    path('my_ads/', my_ads, name='my_ads'),
    path('edit/<int:ad_id>/', edit_ad, name='edit_ad'),
    path('delete/<int:ad_id>/', delete_ad, name='delete_ad'),
    path('proposal/', all_proposals, name='all_proposals'),
    path('proposal/create/<int:ad_id>/', create_proposal, name='create_proposal'),
    path('proposal/update/<int:proposal_id>/', update_proposal_status, name='update_proposal_status')
]
