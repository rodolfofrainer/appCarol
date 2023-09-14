from django.test import TestCase
from .factories import UserFactory
from .models import UserProfileModel

class ORM_Create_update_delete_test(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user_profile = UserProfileModel(user=self.user)
    
    def test_user_creation(self):
        self.assertEqual(self.user.username, self.user_profile.user.username)

    def tearDown(self):
        self.user.delete()
