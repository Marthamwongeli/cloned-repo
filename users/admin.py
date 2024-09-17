from django.contrib import admin
from .models import User  # Import the User model

# Register the User model with the admin site
admin.site.register(User)
