from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from allauth.account import app_settings as allauth_settings

from .models import Role, User

UserModel = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    """
    Responsible for serializing role objects
    """

    class Meta:
        model = Role
        fields = (
            "id",
            "name"
        )
        read_only_fields = ('id',)


class RoleDeleteSerializer(serializers.ModelSerializer):
    """
    Responsible for deleting role instances
    """

    class Meta:
        model = Role
        fields = (
            "id",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Responsible for serializing user objects on create
    """
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "role_id",
            "phone"
        )

    def create(self, validated_data):
        User.objects.create_user(**validated_data)
        return validated_data


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Responsible for Serializing detailed information about User
    """

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "login",
            "password",
            "email",
            "role_id",
            "date_of_add",
            "phone",
        )
        read_only_fields = ("id", "password")


class UserDeleteSerializer(serializers.ModelSerializer):
    """
    Responsible for serializing User objects when deleting
    """

    class Meta:
        model = User
        fields = (
            "id"
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Responsible for Serializing detailed information about User
    """

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "password",
            "email",
            "role_id",
            "phone",
        )
        read_only_fields = ("id",)


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_login(self, login, password):
        user = None

        if login and password:
            user = self.authenticate(username=login, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')

        user = None

        # Authenticate user
        user = self._validate_login(login, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "role_id",
            "phone"
        )

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'role_id': self.validated_data.get('role_id', ''),
            'email': self.validated_data.get('email', ''),
            'phone': self.validated_data.get('phone', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self, True)
        setup_user_email(request, user, [])
        return user
