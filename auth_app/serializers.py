from django.contrib.auth import authenticate
#from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model

User=get_user_model()

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
            raise serializers.ValidationError("A user with this email already exists.")
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
                    raise serializers.ValidationError("Unable to login with given credentials")
            except User.DoesNotExist:
                print(f'User not found')  # Debugging
                raise serializers.ValidationError("Unable to login with given credentials")
        else:
            print(f'Missing email or password')  # Debugging
            raise serializers.ValidationError("Must include 'email' and 'password'")
        return data
