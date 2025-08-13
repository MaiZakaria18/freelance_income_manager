from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id', 'user']

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Category name cannot be empty.")

        user = self.context['request'].user
        if Category.objects.filter(user=user, name__iexact=value).exists():
            raise serializers.ValidationError("You already have a category with this name.")

        return value

