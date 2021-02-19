"""View module for handling requsts about tags"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Tag

class Tags(ViewSet):
    """Rare Tags"""
    def retrieve(self, request, pk=None):
        """Handle GET requests for single tag

        Returns:
            Response --JSON serialized tag
        """
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag, context={'request': request})
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all tags

        Returns:
            Response -- JSON serialized list of tags
        """
        tags = Tag.objects.all()

        # `many=True` argument to the serializer.
        # needed when serializing a list of objects instead of a single object
        serializer = TagSerializer(
            tags, many=True, context={'request': request})
        return Response(serializer.data)
        
class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags

    Arguments: serializers
    """
    class Meta:
        model = Tag
        fields = ('id', 'label')
