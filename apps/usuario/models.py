from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from apps.permiso.models import Permiso

# Create your models here.
class UserManager(BaseUserManager):

  def _create_user(self, email, password):
    if not email:
        raise ValueError('El usuario debe tener un email')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        last_login=now,
        date_joined=now
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password)

class Usuario(AbstractBaseUser):
    nombre = models.CharField(max_length=240)
    email = models.CharField(max_length=240, unique=True)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()