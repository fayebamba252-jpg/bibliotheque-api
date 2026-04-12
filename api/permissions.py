# api/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class EstProprietaireOuReadOnly(BasePermission):
    """
    Règle : lecture libre, mais modification uniquement par le créateur.
    Le modèle doit avoir un champ 'cree_par' ForeignKey vers User.
    """
    message = 'Vous devez être le propriétaire pour modifier cet objet.'

    def has_permission(self, request, view):
        """Permission au niveau de la vue (avant d'accéder à un objet)"""
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Permission au niveau de l'objet (après get_object())"""
        if request.method in SAFE_METHODS:
            return True
        # Modification : uniquement le propriétaire ou un admin
        return obj.cree_par == request.user or request.user.is_staff