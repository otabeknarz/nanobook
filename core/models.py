from django.db import models
from .functions import get_random_id, get_random_promocode


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Promocode(BaseModel):
    class Discounts(models.IntegerChoices):
        D_10 = 10, "10%"
        D_20 = 20, "20%"
        D_30 = 30, "30%"
        D_40 = 40, "40%"

    id = models.CharField(
        default=get_random_id,
        primary_key=True,
        unique=True,
        editable=True,
        max_length=12,
    )
    value = models.CharField(default=get_random_promocode, unique=True, max_length=12)
    discount = models.IntegerField(choices=Discounts.choices)

    def __str__(self):
        return f"{self.value} - {self.discount}"


class Pay(BaseModel):
    id = models.CharField(
        default=get_random_id,
        primary_key=True,
        unique=True,
        editable=True,
        max_length=12,
    )
    # user = models.OneToOneField(CustomUser, related_name="pays")
    value = models.CharField(max_length=32)
    is_done_successfully = models.BooleanField(default=False)
    promocode = models.OneToOneField(
        Promocode, related_name="pay", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.is_done_successfully} - {self.value}"


class Category(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.name


def user_directory_path(instance, filename):
    return f"books/{instance.id}/{filename}"


class Book(BaseModel):
    id = models.CharField(
        default=get_random_id,
        primary_key=True,
        unique=True,
        editable=False,
        max_length=12,
    )
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True)
    # authors = models.ManyToManyField(CustomUser, related_name="books")
    categories = models.ManyToManyField(Category, related_name="books")
    file = models.FileField(upload_to=user_directory_path)
