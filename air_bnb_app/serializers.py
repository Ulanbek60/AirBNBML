from rest_framework import serializers
from .models import UserProfile, Property, Image, Booking, Review
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import joblib
from django.conf import settings
import os

model_path = os.path.join(settings.BASE_DIR, 'model.pkl')
model = joblib.load(model_path)

vec_path = os.path.join(settings.BASE_DIR, 'vec.pkl')
vec = joblib.load(vec_path)

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            user = UserProfile.objects.create_user(**validated_data)
            return user
        except Exception as e:
            return f'{e},   Ощибка при сохранение данных'

    def to_representation(self, instance):
        try:
            refresh = RefreshToken.for_user(instance)
            return {
                'user': {
                    'username': instance.username,
                    'email': instance.email,
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        except Exception as e:
            return f'{e}, Ошибка при создании'




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            request=self.context.get('request'),
            username=data.get('username'),
            password=data.get('password')
        )
        if user is None or not user.is_active:
            raise serializers.ValidationError("Неверные учетные данные")

        refresh = RefreshToken.for_user(user)
        return {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError({'detail': 'Недействительный или уже отозванный токен'})



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'password', 'role', 'phone_number', 'avatar']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'property', 'image']


class PropertySerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'price_per_night', 'city', 'address',
            'property_type', 'rules', 'max_guests', 'bedrooms', 'bathrooms',
            'owner', 'images', 'is_active'
        ]


class BookingSerializer(serializers.ModelSerializer):
    property = serializers.StringRelatedField()
    guest = serializers.StringRelatedField()

    class Meta:
        model = Booking
        fields = ['id', 'property', 'guest', 'check_in', 'check_out', 'status', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    guest = serializers.StringRelatedField(read_only=True)
    property = serializers.StringRelatedField(read_only=True)
    check_comments = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'property', 'guest', 'rating', 'comment', 'created_at', 'check_comments']

    def get_check_comments(self, obj):
         return model.predict(vec.transform([obj.comment]))