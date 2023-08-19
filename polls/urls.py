from django.urls import path
from . import views

urlpatterns = [
    path('', views.polls_list, name='polls_list'),
    path('verify-otp/<int:participant_id>/', views.verify_otp, name='verify_otp'),
    path('completion-page/<int:participant_id>/', views.poll_completion, name='completion_page'),
    path('poll-results/<int:poll_id>/', views.poll_results, name='poll_results'),
]
