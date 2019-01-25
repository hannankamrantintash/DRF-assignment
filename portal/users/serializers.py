from rest_framework import serializers
from users.models import User, Post


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8,
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'cnic', 'created_at', 'updated_at')

    def create(self, validated_data):
        """Creates new user and returns instance of user"""
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """Updates instance of user using validated data"""
        instance.email = validated_data.get(
            'email', instance.email)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.save()
        return instance

    def to_representation(self, value):
        data = super(UserSerializer, self).to_representation(value)
        del data["cnic"]
        return data


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'text', 'created_at', 'updated_at')

    def to_representation(self, value):
        if self.context.get("user") != "AnonymousUser":
            data = super(PostSerializer, self).to_representation(value)
            return data
        elif self.context.get("user") == "AnonymousUser":
            data = super(PostSerializer, self).to_representation(value)
            del data["text"]
            return data
