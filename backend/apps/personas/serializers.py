from rest_framework import serializers
from .models import Persona
from django.utils.text import slugify
import uuid

class PersonaSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Persona
        fields = (
            "id", "name", "slug", "description", "personality_prompt",
            "backstory", "greeting_template", "avatar_url",
            "is_active", "is_public", "creator", "created_at", "updated_at"
        )
        read_only_fields = ("id", "slug", "creator", "created_at", "updated_at")
    
    def create(self, validated_data):
        base_slug = slugify(validated_data["name"])
        slug = base_slug
        if Persona.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
        validated_data["slug"] = slug
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)