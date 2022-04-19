from unittest import skip

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from shop.models import Category, Item
from shop.views import item_list


class TestViewResponses(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
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
        self.c = Client()

    def test_url_allowed_hosts(self):
        """
        Test Item response status
        """
        testResponse = self.c.get('/')
        self.assertEqual(testResponse.status_code, 200)

    def test_item_detail_url(self):
        """
        Test item detail url
        """
        response = self.c.get(reverse('shop:item_detail',args=['django_item']))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        """
        Test category detail url
        """
        response = self.c.get(reverse('shop:category_list',args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        response = item_list(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>GameHUB</title>', html)
        self.assertTrue(html.startswith('\n<!doctype html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        request = self.factory.get('/item/django_item')
        response = item_list(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>GameHUB</title>', html)
        self.assertTrue(html.startswith('\n<!doctype html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/', HTTP_HOST='someaddress.kz')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='game-hub.kz')
        self.assertEqual(response.status_code,200)