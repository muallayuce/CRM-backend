# auth_app/serializers.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

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
                    raise serializers.ValidationError("Unable to login with given credentials")
            except User.DoesNotExist:
                print(f'User not found')  # Debugging
                raise serializers.ValidationError("Unable to login with given credentials")
        else:
            print(f'Missing email or password')  # Debugging
            raise serializers.ValidationError("Must include 'email' and 'password'")
        return data
