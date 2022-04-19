from django.contrib.auth.models import User
from django.test import TestCase

from shop.models import Category, Item


class TestCategoriesModel(TestCase):
    
    def setUp(self):
        self.data1 = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_model_entry(self):
        """
        Test Category model default name
        """
        data = self.data1
        self.assertEqual(str(data), 'django')


class TestItemsModel(TestCase):

    def setUp(self):
        cat = Category.objects.create(name='django', slug='django')
        user = User.objects.create(username='admin')
        self.data1 = Item.objects.create(
            title='django item',
            slug='django_item',
            price=20.00,
            image='django',
            category=cat,
            created_by=user
        )

    def test_items_model_entry(self):
        """
        Test Category model default name
        """
        data = self.data1
        self.assertTrue(isinstance(data, Item))
        self.assertEqual(str(data), 'django item')
        