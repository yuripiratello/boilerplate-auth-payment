from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts.models import Team, Profile

UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=UserModel.objects.all()),
        ],
    )
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserModel
        fields = ("username", "password", "email", "first_name", "last_name")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = ("username", "email", "first_name", "last_name")


class MemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=UserModel.objects.all()),
        ],
    )

    class Meta:
        model = UserModel
        fields = ("username", "email", "first_name", "last_name")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }


class TeamSerializer(serializers.ModelSerializer):
    members = MemberSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Team
        fields = "__all__"
