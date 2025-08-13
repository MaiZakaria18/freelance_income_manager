from rest_framework import serializers
from .models import Project
from datetime import date

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ['id', 'user']

    def validate_payment_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Payment date cannot be in the past.")
        return value

    def validate_project_name(self, value):
        if self.instance:  # If updating
            old_name = self.instance.project_name
            if value == old_name:
                return value

        if Project.objects.filter(project_name=value).exists():
            raise serializers.ValidationError("Project name already exists.")

        return value