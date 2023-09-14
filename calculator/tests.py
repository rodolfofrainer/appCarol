from django.test import TestCase
from django.contrib.auth.models import User
from .models import MarketCreatedModel, ItemCreatedModel
from faker import Faker
import random

fake = Faker()

class ORM_Create_update_delete_test(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = fake.user_name(),
            password = fake.password()
            )
        self.market = MarketCreatedModel.objects.create(
            name=fake.name(),
            distance = random.randint(1,80),
            favorite = False,
            user_id = self.user)
        self.market2 = MarketCreatedModel.objects.create(
            name=fake.name(),
            distance = random.randint(1,80),
            favorite = False,
            user_id = self.user)
        self.item = ItemCreatedModel.objects.create(name=fake.name(),price=random.uniform(0.01, 5000.0), market_id = self.market)

    def test_creation(self):
        #if data was created
        self.assertIsNotNone(self.user)
        self.assertIsNotNone(self.market)
        self.assertIsNotNone(self.item)
    
    def test_market_favorite(self):
        #if market can be favorited
        self.market.favorite = True
        self.market.save()
        self.assertEqual(self.market.favorite, True)

    

    def tearDown(self):
        self.user.delete()
