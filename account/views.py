from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .serializers import RegisterSerializer


class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'user': serializer.data,
            'message': 'User Created Successfully.',
        }, status=status.HTTP_201_CREATED)
