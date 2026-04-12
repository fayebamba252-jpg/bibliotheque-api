# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Auteur, Livre
from .serializers import AuteurSerializer, LivreSerializer, LivreDetailSerializer
from .permissions import EstProprietaireOuReadOnly
from .filters import LivreFilter
from .pagination import StandardPagination


# NIVEAU 1 : APIView 
class AuteurListAPIView(APIView):
    """
    GET  /api/auteurs/   → liste tous les auteurs
    POST /api/auteurs/   → crée un nouvel auteur
    """

    def get(self, request):
        """Retourne la liste de tous les auteurs"""
        auteurs = Auteur.objects.all()
        serializer = AuteurSerializer(auteurs, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Crée un nouvel auteur depuis les données JSON du corps"""
        serializer = AuteurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuteurDetailAPIView(APIView):
    """
    GET    /api/auteurs/{id}/ → détail d'un auteur
    PUT    /api/auteurs/{id}/ → mise à jour complète
    DELETE /api/auteurs/{id}/ → suppression
    """

    def get_object(self, pk):
        """Helper : récupère l'auteur ou lève une 404"""
        try:
            return Auteur.objects.get(pk=pk)
        except Auteur.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound('Auteur non trouvé')

    def get(self, request, pk):
        auteur = self.get_object(pk)
        serializer = AuteurSerializer(auteur)
        return Response(serializer.data)

    def put(self, request, pk):
        auteur = self.get_object(pk)
        serializer = AuteurSerializer(auteur, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        auteur = self.get_object(pk)
        serializer = AuteurSerializer(auteur, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        auteur = self.get_object(pk)
        auteur.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# NIVEAU 2 : Generic Views
class LivreListCreateView(generics.ListCreateAPIView):
    queryset = Livre.objects.all().select_related('auteur')
    serializer_class = LivreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class LivreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer

    def get_serializer_class(self):
        """Retourne un sérialiseur différent selon l'action"""
        if self.request.method == 'GET':
            return LivreDetailSerializer
        return LivreSerializer


#  NIVEAU 3 : ViewSet
class AuteurViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet fournit TOUTES les actions CRUD :
    list, create, retrieve, update, partial_update, destroy
    """
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer

    # Action personnalisée : URL /api/auteurs/{id}/livres/
    @action(detail=True, methods=['get'], url_path='livres')
    def livres(self, request, pk=None):
        """Retourne les livres d'un auteur spécifique"""
        auteur = self.get_object()
        livres = auteur.livres.all()
        serializer = LivreSerializer(livres, many=True)
        return Response(serializer.data)

    # Action non-détail : URL /api/auteurs/stats/
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques globales sur les auteurs"""
        data = {
            'total_auteurs': Auteur.objects.count(),
            'total_livres': Livre.objects.count(),
            'nationalites': list(
                Auteur.objects.values_list('nationalite', flat=True).distinct()
            ),
        }
        return Response(data)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import LivreFilter
from .pagination import StandardPagination


class LivreViewSet(viewsets.ModelViewSet):
    queryset = (
        Livre.objects
        .select_related('auteur')
        .prefetch_related('tags')
        .all()
    )
    serializer_class   = LivreSerializer
    permission_classes = [EstProprietaireOuReadOnly]
    pagination_class   = StandardPagination
    filterset_class    = LivreFilter
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields      = ['titre', 'auteur__nom', 'isbn']
    ordering_fields    = ['titre', 'annee_publication', 'date_creation']
    ordering           = ['-date_creation']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LivreDetailSerializer
        return LivreSerializer

    def perform_create(self, serializer):
        serializer.save(cree_par=self.request.user)

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        qs = self.get_queryset().filter(disponible=True)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def emprunter(self, request, pk=None):
        livre = self.get_object()
        if not livre.disponible:
            return Response(
                {'erreur': "Ce livre n'est pas disponible."},
                status=status.HTTP_400_BAD_REQUEST
            )
        livre.disponible = False
        livre.save()
        return Response({'message': f'Livre "{livre.titre}" emprunté avec succès.'})