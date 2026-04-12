# api/serializers.py
from rest_framework import serializers
from .models import Auteur, Livre, Tag


# ─── Serializer de base (déclaratif) ─────────────────────────────────────
class AuteurSimpleSerializer(serializers.Serializer):
    id          = serializers.IntegerField(read_only=True)
    nom         = serializers.CharField(max_length=200)
    nationalite = serializers.CharField(max_length=100, required=False)

    def create(self, validated_data):
        return Auteur.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nom         = validated_data.get('nom', instance.nom)
        instance.nationalite = validated_data.get('nationalite', instance.nationalite)
        instance.save()
        return instance


# ─── ModelSerializer Auteur ───────────────────────────────────────────────
class AuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Auteur
        fields = '__all__'
        read_only_fields = ['id', 'date_creation']


# ─── Serializer Tag ───────────────────────────────────────────────────────
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Tag
        fields = ['id', 'nom']


# ─── Serializer Livre avec validation et tags ─────────────────────────────
class LivreSerializer(serializers.ModelSerializer):
    # Champ calculé (lecture seule)
    auteur_nom = serializers.SerializerMethodField()

    # Tags imbriqués en lecture
    tags = TagSerializer(many=True, read_only=True)

    # Tags IDs pour l'écriture
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        source='tags',
        write_only=True,
        required=False
    )

    class Meta:
        model  = Livre
        fields = [
            'id', 'titre', 'isbn', 'annee_publication',
            'categorie', 'auteur', 'auteur_nom',
            'disponible', 'tags', 'tag_ids'
        ]
        read_only_fields = ['id']

    def get_auteur_nom(self, obj):
        return obj.auteur.nom

    def validate_isbn(self, value):
        clean = value.replace('-', '')
        if not clean.isdigit() or len(clean) != 13:
            raise serializers.ValidationError(
                "L'ISBN doit contenir exactement 13 chiffres."
            )
        return value

    def validate_annee_publication(self, value):
        if value < 1000 or value > 2025:
            raise serializers.ValidationError(
                "L'année doit être entre 1000 et 2025."
            )
        return value

    def validate(self, data):
        if data.get('categorie') == 'essai':
            auteur = data.get('auteur')
            if auteur and not auteur.biographie:
                raise serializers.ValidationError(
                    "Les essais requièrent une biographie de l'auteur."
                )
        return data


# ─── Serializer imbriqué ─────────────────────────────────────────────────
class LivreDetailSerializer(serializers.ModelSerializer):
    auteur    = AuteurSerializer(read_only=True)
    auteur_id = serializers.PrimaryKeyRelatedField(
        queryset=Auteur.objects.all(),
        source='auteur',
        write_only=True
    )
    tags   = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        source='tags',
        write_only=True,
        required=False
    )

    class Meta:
        model  = Livre
        fields = [
            'id', 'titre', 'isbn', 'annee_publication',
            'categorie', 'auteur', 'auteur_id',
            'disponible', 'tags', 'tag_ids'
        ]