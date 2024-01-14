from django.test import TestCase
from base.models import User, Servicer

class UserModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password123',
            first_name='John',
            last_name='Doe',
            phone_number='1234567890',
            username='john_doe',
        )

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        saved_user = User.objects.get(email='test@example.com')
        self.assertEqual(saved_user.first_name, 'John')
        # Add more assertions based on your model fields

class ServicerModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            email='servicer@example.com',
            password='servicer123',
            first_name='Servicer',
            last_name='Test',
            phone_number='9876543210',
            username='servicer_test',
        )
        # Create a servicer linked to the user
        self.servicer = Servicer.objects.create(user=self.user)

    def test_servicer_creation(self):
        self.assertEqual(Servicer.objects.count(), 1)
        saved_servicer = Servicer.objects.get(user__email='servicer@example.com')
        self.assertEqual(saved_servicer.user.first_name, 'Servicer')
        # Add more assertions based on your model fields
