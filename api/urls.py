# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuteurListAPIView, AuteurDetailAPIView,
    LivreListCreateView, LivreDetailView,
    AuteurViewSet, LivreViewSet
)

# Crée un router qui génère les URLs automatiquement
router = DefaultRouter()
router.register(r'auteurs', AuteurViewSet, basename='auteur')
router.register(r'livres',  LivreViewSet,  basename='livre')

urlpatterns = [
    # URLs générées automatiquement par le Router
    path('', include(router.urls)),

    # URLs manuelles avec APIView
    path('auteurs-api/',          AuteurListAPIView.as_view(),   name='auteur-list'),
    path('auteurs-api/<int:pk>/', AuteurDetailAPIView.as_view(), name='auteur-detail'),

    # URLs avec Generic Views
    path('livres-api/',           LivreListCreateView.as_view(), name='livre-list'),
    path('livres-api/<int:pk>/',  LivreDetailView.as_view(),     name='livre-detail'),
]
# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    AuteurListAPIView, AuteurDetailAPIView,
    LivreListCreateView, LivreDetailView,
    AuteurViewSet, LivreViewSet
)

# Crée un router qui génère les URLs automatiquement
router = DefaultRouter()
router.register(r'auteurs', AuteurViewSet, basename='auteur')
router.register(r'livres',  LivreViewSet,  basename='livre')

urlpatterns = [
    # URLs générées automatiquement par le Router
    path('', include(router.urls)),

    # URLs manuelles avec APIView
    path('auteurs-api/',          AuteurListAPIView.as_view(),   name='auteur-list'),
    path('auteurs-api/<int:pk>/', AuteurDetailAPIView.as_view(), name='auteur-detail'),

    # URLs avec Generic Views
    path('livres-api/',           LivreListCreateView.as_view(), name='livre-list'),
    path('livres-api/<int:pk>/',  LivreDetailView.as_view(),     name='livre-detail'),

    # URLs JWT
    path('auth/token/',         TokenObtainPairView.as_view(),  name='token_obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),     name='token_refresh'),
]