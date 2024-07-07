from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from PIL import Image as PILImage
from io import BytesIO

from .models import Image
from .serializers import ImageSerializer
from utils.response import APIResponseMixin

class ImageViewSet(APIResponseMixin, mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.api_response(data=serializer.data)

    def perform_create(self, serializer):
        image_instance = serializer.save()
        image = PILImage.open(image_instance.image.path)
        
        image.thumbnail((1024, 1024))
        image_format = 'WEBP'
        
        output_io = BytesIO()
        image.save(output_io, format=image_format)
        output_io.seek(0)
        
        image_instance.image.save(f"{image_instance.id}.{image_format.lower()}", output_io, save=False)
        image_instance.save()
