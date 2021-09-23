from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
from accounts.models import User, Profile
from accounts.serializars import ProfileSerializer


class UserProfileView(APIView):

    def get(self, request, pk):
        profile = get_object_or_404(Profile, user__pk=pk)
        serializador = ProfileSerializer(profile)

        return Response(serializador.data)
