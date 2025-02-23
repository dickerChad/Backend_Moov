from rest_framework.serializers import ModelSerializer
from gestion.models import User, Projet, Departement, Document, Tache
from rest_framework import serializers


class DepartementSerializer(ModelSerializer):
    class Meta:
        model = Departement
        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    prenom = serializers.CharField()
    nom = serializers.CharField()
    sexe = serializers.CharField()
    role = serializers.CharField()


class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        extra_kwargs = {'password': {
            'write_only': True,
            'required': True
        }
        }

class UserSerialiserUpdate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","is_active","role")

class ProjetSerializer(ModelSerializer):
    user = UserSerialiser(read_only=True)
    departement = DepartementSerializer(read_only=True)
    class Meta:
        model = Projet
        fields = ("id", "nom", "date_debut", "date_fin", "description", "user", "departement", "etat", "statut")
        # read_only_field = ['user', 'departement']
        depth = 1

class ProjetSerializerUpdate(ModelSerializer):
    class Meta:
        model = Projet
        fields = ("id", "nom", "date_debut", "date_fin", "description", "departement")


class ProjetSerializerCreate(ModelSerializer):
    class Meta:
        model = Projet
        fields = '__all__'

class ProjetSerializerUpdateStatut(ModelSerializer):
    class Meta:
        model = Projet
        fields = ("id","statut")
        


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class TacheSerializer(ModelSerializer):
    # projet = ProjetSerializer(read_only=True)
    class Meta:
        model = Tache
        fields = '__all__'

class TacheSerializerUpdated(ModelSerializer):
    # projet = ProjetSerializer(read_only=True)
    class Meta:
        model = Tache
        fields = ("id", "estRealisee")
