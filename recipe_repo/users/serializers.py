from __future__ import annotations

from rest_framework import serializers

from .models import Comment, User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "full_name", "initials", "profile_image_url", "is_staff")


class CommentSerializer(serializers.ModelSerializer[Comment]):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("user", "text", "created")
