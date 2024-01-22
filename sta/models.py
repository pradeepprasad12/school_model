from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, phone_number=None, user_type=None):
        """
        Creates and saves a User with the given email, name, password, phone_number, and user_type.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_number=phone_number,
            user_type=user_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, phone_number=None, user_type=None):
        """
        Creates and saves a superuser with the given email, name, password, phone_number, and user_type.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            phone_number=phone_number,
            user_type=user_type,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, unique=True)
    user_type = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')])
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number', 'user_type']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class ImageUpload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='image_uploads')
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"

    def user_image_path(instance, filename):
        return f'user_images/{instance.user.email}/{filename}'

    image = models.ImageField(upload_to=user_image_path)
