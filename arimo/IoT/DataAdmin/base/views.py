from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token
from django.http import HttpResponse, Http404, JsonResponse

from rest_framework import status
from rest_framework.generics import \
    ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import EquipmentGeneralType
from .serializers import EquipmentGeneralTypeSerializer


class EquipmentGeneralTypeList(APIView):
    pass