from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UserSerialiser, ProjetSerializer, ProjetSerializerCreate, RegisterSerializer, DepartementSerializer, DocumentSerializer, TacheSerializer, TacheSerializerUpdated, ProjetSerializerUpdateStatut,ProjetSerializerUpdate,UserSerialiserUpdate
from gestion.models import User, Projet, Departement, Document, Tache
from django.db.models import Sum



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['nom'] = user.nom
        token['prenom'] = user.prenom
        token['role'] = user.role
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(APIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects._create_user(**serializer.validated_data)
        if user:
            return Response({'Success: ' : 'User Created Successfully...!'}, status=status.HTTP_201_CREATED)
        return Response({'Failed: ' : 'User Created Failed...!'}, status=status.HTTP_400_BAD_REQUEST)

class UpdateView(APIView):
    serializer_class= UserSerialiser
    def put(self, request,pk):
        user = User.objects.get(pk=pk)
        serializer = self.serializer_class(instance = user,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        if user:
            return Response({'Success: ' : 'User Updated Successfully...!'}, status=status.HTTP_201_CREATED)
        return Response({'Failed: ' : 'User Updated Failed...!'}, status=status.HTTP_400_BAD_REQUEST)

class UpdateUser(APIView):
    serializer_class= UserSerialiserUpdate
    def put(self, request,pk):
        user = User.objects.get(pk=pk)
        serializer = self.serializer_class(instance = user,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        if user:
            return Response({'Success: ' : 'User Updated Successfully...!'}, status=status.HTTP_201_CREATED)
        return Response({'Failed: ' : 'User Updated Failed...!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'api/token',
        'api/token/refresh',
    ]
    return Response(routes)

@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerialiser(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerialiser(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateUser(request, pk):
    data = request.data
    user = User.objects.get(id=pk)
    serializer = UserSerialiser(instance = user, data=data)
    
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return Response("user was delete")

# @api_view(['POST'])
# def createUser(request):
#     serializerUser = RegisterSerializer(data=request.data)
#     if serializerUser.is_valid(raise_exception=True):
#         user = User.objects._create_user(**serializerUser.validated_data)
#         return Response(200)
#     return Response(serializerUser.errors)
from django.db.models import Q

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getProjets(request):
    projets = Projet.objects.all()
    # projets = Projet.objects.filter(Q(user=request.user))
    serializer = ProjetSerializer(projets, many=True)
    # serializerAll = ProjetSerializer(projetAll, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProjet(request, pk):
    # projet = Projet.objects.filter(Q(user=request.user)).get(id=pk)
    projet = Projet.objects.get(id=pk)
    serializer = ProjetSerializer(projet, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createProjet(request):
    serializerProjet = ProjetSerializerCreate(data=request.data)
    if serializerProjet.is_valid(raise_exception=True):
        serializerProjet.save()
        return Response(200)
    return Response(serializerUser.errors)


@api_view(['PUT'])
def updateprojet(request, pk):
    projet = Projet.objects.get(pk=pk)
    serializer = ProjetSerializer(projet, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteProjet(request, pk):
    projet = Projet.objects.get(id=pk)
    projet.delete()
    return Response("projet was delete")


# @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# def getRoles(request):
#     roles = Role.objects.all()
#     serializer = RoleSerializer(roles, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getDepartements(request):
    departements = Departement.objects.all()
    serializer = DepartementSerializer(departements, many=True)
    return Response(serializer.data)


class projetTable(APIView):
    def get(self, request):
        projet=Projet.objects.all()
        serializer = ProjetSerializer(projet, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializerProjet = ProjetSerializerCreate(data=request.data)
        if serializerProjet.is_valid():
            serializerProjet.save()
            return Response(200)
        return Response(serializerProjet.errors)

class projetUpdate(APIView):
    def post(self, request,pk):
        try:
            projet = Projet.objects.get(pk=pk)
        except:
            return Response("Not found")

        serializerProjet = ProjetSerializer(projet, data=request.data)
        if serializerProjet.is_valid():
            serializerProjet.save()
            return Response(200)
        return Response(serializerProjet.errors)

class projetUpdateStatut(APIView):
    def post(self, request,pk):
        try:
            projet = Projet.objects.get(pk=pk)
        except:
            return Response("Not found")

        serializerProjetStatut = ProjetSerializerUpdateStatut(projet, data=request.data)
        if serializerProjetStatut.is_valid():
            serializerProjetStatut.save()
            return Response(200)
        return Response(serializerProjetStatut.errors)

class UpdateProjetView(APIView):
    serializer_class= ProjetSerializerUpdate
    def put(self, request,pk=None):
        projet = Projet.objects.get(pk=pk)
        serializer = self.serializer_class(instance = projet,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        if projet:
            return Response({'Success: ' : 'Projet Updated Successfully...!'}, status=status.HTTP_201_CREATED)
        return Response({'Failed: ' : 'Projet Updated Failed...!'}, status=status.HTTP_400_BAD_REQUEST)


class departementUpdate(APIView):
    def post(self, request,pk):
        try:
            departement = Departement.objects.get(pk=pk)
        except:
            return Response("Not found")

        serializerDepartement = DepartementSerializer(departement, data=request.data)
        if serializerDepartement.is_valid():
            serializerDepartement.save()
            return Response(200)
        return Response(serializerDepartement.errors)

class documentUpdate(APIView):
    def post(self, request,pk):
        try:
            document = Document.objects.get(pk=pk)
        except:
            return Response("Not found")

        serializerDocument = DocumentSerializer(document, data=request.data)
        if serializerDocument.is_valid():
            serializerDocument.save()
            return Response(200)
        return Response(serializerDocument.errors)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getDocuments(request,pk):
    projet = Projet.objects.get(id=pk)
    documents = Document.objects.filter(Q(projet=projet))
    serializer = DocumentSerializer(documents, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTaches(request,pk):
    projet = Projet.objects.get(id=pk)
    taches = Tache.objects.filter(Q(projet=projet))
    tache = Tache.objects.filter(Q(projet=projet) & Q(estRealisee=True))
    serializer = TacheSerializer(taches, many=True)
    all_sum = tache.aggregate(Sum('valeur'))
    return Response({'sum': all_sum if all_sum else 0 , 'objects':serializer.data})

@api_view(['POST'])
def createTache(request):
    serializerTache = TacheSerializer(data=request.data)
    if serializerTache.is_valid(raise_exception=True):
        serializerTache.save()
        return Response(200)
    return Response(serializerTache.errors)

class TacheUpdate(APIView):
    def post(self, request,pk):
        try:
            tache = Tache.objects.get(pk=pk)
        except:
            return Response("Not found")

        serializerTache = TacheSerializerUpdated(tache, data=request.data)
        if serializerTache.is_valid():
            serializerTache.save()
            return Response(200)
        return Response(serializerTache.errors)

@api_view(['DELETE'])
def deleteTache(request, pk):
    tache = Tache.objects.get(id=pk)
    tache.delete()
    return Response("tache was delete")
