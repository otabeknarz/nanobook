from .functions import get_random_id, get_random_promocode
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PromoCode(BaseModel):
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
    user = models.OneToOneField("CustomUser", related_name="pays", on_delete=models.CASCADE)
    value = models.CharField(max_length=32)
    is_done_successfully = models.BooleanField(default=False)
    promo_code = models.OneToOneField(
        PromoCode, related_name="pay", null=True, blank=True, on_delete=models.SET_NULL
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
    authors = models.ManyToManyField("CustomUser", related_name="books")
    categories = models.ManyToManyField(Category, related_name="books")
    file = models.FileField(upload_to=user_directory_path)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, phone_number=None, password=None, **extra_fields):
        if not username:
            raise ValueError(_('The Username field must be set'))
        if not phone_number:
            raise ValueError(_('The Phone Number field must be set'))

        user = self.model(username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(_('username'), max_length=150, unique=True)
    phone_number = models.CharField(_('phone number'), max_length=15, unique=True, blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username