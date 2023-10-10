import json
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import (
    RegisterSerializer,
    UserSerializer,
    TeamSerializer,
    MemberSerializer,
)
from accounts.models import Team


class MyTeamView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        my_team, _ = Team.objects.get_or_create(owner=request.user)
        return Response(
            data={"team": TeamSerializer(my_team).data},
            status=status.HTTP_200_OK,
        )


class NewTeamMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        member_data = MemberSerializer(data=request.data)
        if not member_data.is_valid():
            return Response(
                data=member_data.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        with transaction.atomic():
            team, _ = Team.objects.get_or_create(owner=request.user)
            team.create_and_add_member(member_data.validated_data)
            return Response(
                data={"team": TeamSerializer(team).data},
                status=status.HTTP_200_OK,
            )


class UserRegistrationView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        if request.auth is None:
            data = request.data
            serializer = RegisterSerializer(data=data)
            if not serializer.is_valid():
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            try:
                with transaction.atomic():
                    user = serializer.save()
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            "token": {
                                "refresh": str(refresh),
                                "access": str(refresh.access_token),
                            },
                            "user": UserSerializer(user).data,
                        },
                        status=status.HTTP_201_CREATED,
                    )
            except Exception as e:
                return Response(
                    data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(status=status.HTTP_403_FORBIDDEN)
