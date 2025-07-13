from rest_framework import serializers
from .models import Product, Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)  # remove source

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'average_rating']
