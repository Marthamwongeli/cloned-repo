from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):
    
    def setUp(self):
        """
        Set up initial test data.
        """
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='password123',
            first_name='Test',
            last_name='User',
            phone_number='1234567890',
            user_role='nurse'
        )
    
    def test_user_creation(self):
        """
        Test that a user can be created successfully.
        """
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('password123'))
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertEqual(self.user.user_role, 'nurse')

    def test_superuser_creation(self):
        """
        Test that a superuser can be created and has the correct attributes.
        """
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='adminuser',
            password='adminpass'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.email, 'admin@example.com')

    def test_user_without_email_fails(self):
        """
        Test that creating a user without an email raises a ValueError.
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                username='nouser',
                password='password123'
            )
    
    def test_user_string_representation(self):
        """
        Test the __str__ method of the User model.
        """
        self.assertEqual(str(self.user), 'testuser')

    def test_user_role_assignment(self):
        """
        Test that the user role can be assigned correctly.
        """
        self.assertEqual(self.user.user_role, 'nurse')
        # Change role and test again
        self.user.user_role = 'admin'
        self.user.save()
        self.assertEqual(self.user.user_role, 'admin')

    def test_required_fields(self):
        """
        Test that required fields are properly validated.
        """
        # Username and email are required fields
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username='',
                email='',
                password='password123'
            )
