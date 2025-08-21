from rest_framework import serializers
from .models import Tip, TipRating

class TipSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Tip
        fields = ['id', 'category', 'user_email', 'text', 'created_at', 'average_rating']
        read_only_fields = ['created_at', 'average_rating']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TipRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipRating
        fields = ['id', 'tip', 'user', 'value', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate_value(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        request = self.context['request']
        user = request.user
        tip = data['tip']

        if tip.user == user:
            raise serializers.ValidationError("You cannot rate your own tip.")

        if TipRating.objects.filter(user=user, tip=tip).exists():
            raise serializers.ValidationError("You have already rated this tip.")

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)



