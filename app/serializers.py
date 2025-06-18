from rest_framework import serializers
from .models import CustomUser, Tea
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False, 'default': ''},
            'last_name': {'required': False, 'default': ''},
            'role': {'required': False, 'default': 'user'}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)  # Remove password2 as it's not a model field
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'user')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'role')

class TeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tea
        fields = '__all__'
