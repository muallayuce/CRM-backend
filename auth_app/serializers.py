from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists.")
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        print(f'Attempting login with email: {email} and password: {password}')

        if email and password:
            try:
                user = User.objects.get(email=email)
                print(f'User found: {user}')  # Debugging
                if user.check_password(password):
                    data['user'] = user
                    print(f'Password check passed')  # Debugging
                else:
                    print(f'Password check failed')  # Debugging
                    raise serializers.ValidationError(
                        "Unable to login with given credentials")
            except User.DoesNotExist:
                print(f'User not found')  # Debugging
                raise serializers.ValidationError(
                    "Unable to login with given credentials")
        else:
            print(f'Missing email or password')  # Debugging
            raise serializers.ValidationError(
                "Must include 'email' and 'password'")
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate(self, data):
        user = self.context['request'].user

        # Debugging: Check what user is retrieved
        print(f"Authenticated user: {user}")

        if not user.check_password(data['old_password']):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return data

class ChangePasswordByIdSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate(self, data):
        user = self.context['user']

        if not user.check_password(data['old_password']):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return data
