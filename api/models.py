# -*- coding: utf-8 -*-
# api/models.py
from django.db import models
from django.contrib.auth.models import User


class Auteur(models.Model):
    """
    Représente un auteur de livres.
    Django crée automatiquement un champ 'id' (clé primaire).
    """

    nom = models.CharField(
        max_length=200,
        verbose_name='Nom complet'
    )

    biographie = models.TextField(
        blank=True,
        null=True,
        verbose_name='Biographie'
    )

    nationalite = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='Nationalité'
    )

    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']
        verbose_name = 'Auteur'
        verbose_name_plural = 'Auteurs'

class Tag(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom

class Livre(models.Model):
    """
    Représente un livre. Chaque livre a UN auteur (ForeignKey = N vers 1).
    Un auteur peut avoir PLUSIEURS livres.
    """

    CATEGORIES = [
        ('roman',    'Roman'),
        ('essai',    'Essai'),
        ('poesie',   'Poésie'),
        ('bd',       'Bande dessinée'),
        ('science',  'Science'),
        ('histoire', 'Histoire'),
    ]

    titre = models.CharField(max_length=300, verbose_name='Titre')

    isbn = models.CharField(
        max_length=17,
        unique=True,
        verbose_name='ISBN'
    )

    annee_publication = models.IntegerField(
        verbose_name='Année de publication'
    )

    categorie = models.CharField(
        max_length=20,
        choices=CATEGORIES,
        default='roman',
        verbose_name='Catégorie'
    )

    auteur = models.ForeignKey(
        Auteur,
        on_delete=models.CASCADE,
        related_name='livres',
        verbose_name='Auteur'
    )
    # ManyToMany : un livre peut avoir plusieurs tags, un tag plusieurs livres
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='livres'
    )

    cree_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='livres_crees',
        verbose_name='Créé par'
    )

    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titre} ({self.annee_publication})'

    class Meta:
        ordering = ['-annee_publication', 'titre']


class Emprunt(models.Model):
    """
    Représente un emprunt de livre par un utilisateur.
    """

    utilisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='emprunts',
        verbose_name='Utilisateur'
    )

    livre = models.ForeignKey(
        Livre,
        on_delete=models.CASCADE,
        related_name='emprunts',
        verbose_name='Livre'
    )

    date_emprunt = models.DateField(
        auto_now_add=True,
        verbose_name='Date d emprunt'
    )

    date_retour_prevue = models.DateField(
        verbose_name='Date de retour prévue'
    )

    rendu = models.BooleanField(
        default=False,
        verbose_name='Rendu'
    )

    def __str__(self):
        return f'{self.utilisateur} — {self.livre} — {self.date_emprunt}'

    class Meta:
        ordering = ['-date_emprunt']
        verbose_name = 'Emprunt'
        verbose_name_plural = 'Emprunts'