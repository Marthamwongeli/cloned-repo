from django.urls import path
from .views import UserListView, UserDetailView
from . import views
from .views import LoginView
from .views import LogoutView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView
from .views import UserRoleListCreateView
from .views import UserProfileView




urlpatterns = [
    path('users/', UserListView.as_view(), name='user_view'),  # For POST and GET (authenticated user)
    path('user/<int:id>/', UserDetailView.as_view(), name='user_detail_view'),  # For GET, PATCH (user by ID)
    path('generate_token/', views.generate_token, name='generate_token'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/logout/', LogoutView.as_view(), name='logout'),
    path('users/roles/', UserRoleListCreateView.as_view(), name='user_roles'),
    path('users/profile/', UserProfileView.as_view(), name='user_profile'),
    




]
