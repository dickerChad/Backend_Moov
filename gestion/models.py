from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email Field is required...!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super User must be a staff.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super User must be a Super User.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Super User must be Active.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    
    Roles = (
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('EMPLOYE', 'Employe'),
    )

    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=255, blank=True, null=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    GENDER_CHOICES = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )
    sexe = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    role = models.CharField(max_length=50, choices=Roles, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField('User Image',upload_to="images/", blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Departement(models.Model):
    nom = models.CharField('Name Departement', max_length=50)

    def __str__(self):
        return self.nom


class Projet(models.Model):
    nom = models.CharField('ProjectName', max_length=100)
    date_debut = models.DateField('StartDateProject')
    date_fin = models.DateField('EndDateProjects')
    description = models.CharField('ProjectDescription ', max_length=500)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    etat = models.BooleanField(default=False)
    class Statut(models.TextChoices):
        NON_DEMARRE = "NON_DEMARRE", 'non_demarre'
        EN_COURS = "EN_COURS", 'en_cours'
        TERMINE = "TERMINE", 'termine'

    base_statut = Statut.NON_DEMARRE

    statut = models.CharField(max_length=40, choices=Statut.choices, default=Statut.NON_DEMARRE)

    def __str__(self):
        return self.nom

class Document(models.Model):
    nom_doc = models.CharField('Name Document', max_length=50)
    doc = models.FileField(upload_to='docs/')
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)


    def __str__(self):
        return self.nom_doc


class Tache(models.Model):
    nom = models.CharField('Task Name', max_length=50)
    valeur = models.FloatField('Percent Project')
    estRealisee = models.BooleanField(default=False)
    date_debut = models.DateField('Start Date Task')
    date_fin = models.DateField('End Date Task')
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom



