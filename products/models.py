from django.db import models


class ProductManager(models.Manager):
    def all(self):
        return super(ProductManager, self).filter(active=True).exclude(price=None).exclude(price=0)

    def custom_all(self):
        return super(ProductManager, self).filter(active=True).exclude(price=None).exclude(price=0).exclude(description="")


class Product(models.Model):
    title = models.CharField(max_length=220)
    description = models.CharField(max_length=3000, null=-True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)

    objects = ProductManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']


class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    description = models.CharField(max_length=3000, null=-True, blank=True)
    image = models.ImageField(upload_to='product/images/')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return unicode(self.image)