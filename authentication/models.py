import logging
from django.contrib.auth.models import AbstractUser
from django.db import models

# Set up logging
logger = logging.getLogger(__name__)

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser to include additional fields and customization.
    """ 
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    
    def __str__(self):
        """
        Return the string representation of the user.
        """
        logger.debug('Generating string representation of user: %s', self.username)
        return self.username
    
    def save(self, *args, **kwargs):
        """
        Override the save method to add custom behavior before saving the user instance.
        """
        # Log when a user instance is being saved
        logger.info('Saving user instance: %s', self.username)
        super().save(*args, **kwargs)
        # Optionally, log after the instance is saved if needed
        logger.info('User instance saved successfully: %s', self.username)
        
    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
        # Additional meta options can be added here