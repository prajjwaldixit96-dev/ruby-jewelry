from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):

    TAG_CHOICES = [
        ('', 'None'),
        ('bestseller', 'Bestseller'),
        ('new', 'New Arrival'),
    ]

    title       = models.CharField(max_length=200)
    price       = models.IntegerField()
    description = models.TextField()
    image       = models.ImageField(upload_to='products/', blank=True, null=True)
    category    = models.ForeignKey(
                    Category,
                    on_delete=models.SET_NULL,
                    null=True, blank=True
                  )
    tag         = models.CharField(max_length=20, choices=TAG_CHOICES, default='', blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
