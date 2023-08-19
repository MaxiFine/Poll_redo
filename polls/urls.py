from django.urls import path
from .views import (HomePageView, polls_list, verify_otp, 
                    poll_completion, poll_results)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('polls-list', polls_list, name='polls_list'),
    path('verify-otp/<int:participant_id>/', verify_otp, name='verify_otp'),
    path('completion-page/<int:participant_id>/', poll_completion, name='completion_page'),
    path('poll-results/<int:poll_id>/', poll_results, name='poll_results'),
]
