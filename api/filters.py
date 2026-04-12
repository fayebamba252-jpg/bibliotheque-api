# api/filters.py
import django_filters
from .models import Livre


class LivreFilter(django_filters.FilterSet):
    """
    Permet de filtrer les livres via des paramètres URL.
    Exemple : GET /api/livres/?categorie=roman&annee_min=1990&titre=misérables
    """

    # Filtre exact sur un champ
    categorie = django_filters.ChoiceFilter(choices=Livre.CATEGORIES)

    # Filtres de plage sur un entier
    annee_min = django_filters.NumberFilter(
        field_name='annee_publication',
        lookup_expr='gte'
    )
    annee_max = django_filters.NumberFilter(
        field_name='annee_publication',
        lookup_expr='lte'
    )

    # Filtre insensible à la casse
    titre = django_filters.CharFilter(lookup_expr='icontains')

    # Filtre sur une relation (nom de l'auteur)
    auteur_nom = django_filters.CharFilter(
        field_name='auteur__nom',
        lookup_expr='icontains'
    )

    # Filtre booléen
    disponible = django_filters.BooleanFilter()

    class Meta:
        model  = Livre
        fields = ['categorie', 'disponible']