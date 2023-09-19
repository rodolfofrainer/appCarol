from django.test import TestCase
from django.contrib.auth.models import User
from .factories import UserFactory, MarketCreatedFactory, ItemCreatedFactory
from faker import Faker

fake = Faker()


class ORM_Create_update_delete_test(TestCase):
    def setUp(self):
        self.user = UserFactory()

        self.market = MarketCreatedFactory()
        self.market2 = MarketCreatedFactory()
        self.item = ItemCreatedFactory()

    def test_creation(self):
        # if data was created
        self.assertIsNotNone(self.user)
        self.assertIsNotNone(self.market)
        self.assertIsNotNone(self.item)

    def test_market_favorite(self):
        # if market can be favorited
        self.market.favorite = True
        self.market.save()
        self.assertEqual(self.market.favorite, True)

    def test_second_market_favorite(self):
        # if market 2 is favorited, market 1 is unfavorited
        self.market2.favorite = True
        self.market.save()
        self.market.refresh_from_db()
        self.assertEqual(self.market.favorite, False)

    def tearDown(self):
        self.user.delete()
