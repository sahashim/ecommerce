from django.db import models
# Create your models here.
from django.db.models import PROTECT

from core.models import BaseModel, BaseDiscount


class Discount(BaseDiscount):
    """
    The model for discount, this will not have any extra fields.
    """
    ...

    def discounted_price(self, price: int) -> int:
        """
        Calculate the price after discount
        :param price: product price
        :return: discounted price
        """
        if self.type == 'val':
            if price < self.amount:
                # More discount than price
                return price
            return int(price - int(self.amount))
        elif self.type == "cent":
            return price - int((self.amount / 100) * price)

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'

    def __str__(self):
        return f"Discount type: {self.type} Amount: {self.amount}"


class Brand(BaseModel):
    """
    The model for brands.
    """
    discount = models.OneToOneField(to=Discount, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=50, default='', help_text="Name of brand")

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return f"Brand: {self.name}"


class Category(BaseModel):
    """
    The model for Categories.
    """
    discount = models.OneToOneField(to=Discount, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=50, default='', help_text="Name of Category")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Parent Category', null=True, blank=True)
    image = models.FileField(null=True, default=None, upload_to='category/', blank=True)

    def __str__(self):
        return f"Category: {self.name}"

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Comment(BaseModel):
    """
    The model for comments.
    """
    content = models.CharField(max_length=250, null=True, default='So far so good', help_text="Comment text")

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Comment: {self.content}"


class Product(BaseModel):
    """
    The model for products.
    """
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT)
    brand = models.ForeignKey(to=Brand, on_delete=models.PROTECT)
    discount = models.OneToOneField(to=Discount, on_delete=models.PROTECT, null=True, blank=True)
    comment = models.ForeignKey(to=Comment, on_delete=PROTECT, null=True, blank=True)
    name = models.CharField(max_length=50, default='', help_text="Name of product")
    image = models.FileField(null=True, default=None, upload_to='product/', blank=True)
    price = models.PositiveIntegerField(default=0, null=False, help_text="Price of product")
    description = models.CharField(max_length=250, help_text="Product description", default="description")
    count = models.PositiveIntegerField(default=1, null=False, help_text="Count of product")

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.brand.name} {self.name} with price of {self.price}"

    @property
    def calc_discounted(self):
        if self.discount is not None:
            return self.discount.discounted_price(int(self.price))
        else:
            return self.price
