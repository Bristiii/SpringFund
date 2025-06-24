from django.urls import path
from .views import RegisterView, LoginView, SavedFundView, SavedFundDetailView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('saved-funds/', SavedFundView.as_view(), name='saved-fund-list'),
    path('saved-funds/<int:pk>/', SavedFundDetailView.as_view(), name='saved-fund-detail'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
