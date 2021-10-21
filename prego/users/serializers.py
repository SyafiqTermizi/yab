from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import User


class UserCreationSerializer(serializers.ModelSerializer):
    password_1 = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    password_2 = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password_1", "password_2")

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                detail="User with given username already exist",
                code="user_exist",
            )
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                detail="User with given username already exist",
                code="user_exist",
            )
        return email

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        if validated_data["password_1"] != validated_data["password_2"]:
            raise serializers.ValidationError(
                detail="Password Not Match",
                code="password_mismatch",
            )
        validate_password(validated_data["password_1"])
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password_1"],
        )


class AuthenticationSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(required=True)
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )

    is_email = False
    user = None

    def validate_username_or_email(self, username_or_email):
        try:
            validate_email(username_or_email)
        except ValidationError:
            pass
        else:
            self.is_email = True
        return username_or_email

    def validate(self, attrs):
        validated_attrs = super().validate(attrs)

        if self.is_email:
            user = authenticate(
                email=validated_attrs["username_or_email"],
                password=validated_attrs["password"],
            )
        else:
            user = authenticate(
                username=validated_attrs["username_or_email"],
                password=validated_attrs["password"],
            )

        if not user:
            raise serializers.ValidationError("Invalid Username or password")

        self.user = user
        return validated_attrs


class FindUserByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    user = None

    def validate_email(self, email: str):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with given email does not exist")
        else:
            self.user = user
        return email
