from django.conf import settings
from django.db import models
from django.urls import reverse


class ItemManager(models.Manager):
    def get_queryset(self):
        return super(ItemManager, self).get_queryset().filter(is_active=True)

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('shop:category_list',args=[self.slug])

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='item', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='item_creator', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/item_pics/', default='images/item_pics/default.png')
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    items = ItemManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Items'
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('shop:item_detail',args=[self.slug])