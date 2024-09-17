
# urls.py
from django.urls import path
from .views import login, callback, logout, index

urlpatterns = [
    path('api/users/login/', login, name='login'),         # OAuth login
    path('api/users/callback/', callback, name='callback'),  # OAuth callback
    path('api/users/logout/', logout, name='logout'),      # Logout route
    path('', index, name='index'),                         # Index page
]
