"""View module for handling requsts about tags"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Tag, Post, PostTag

class Tags(ViewSet):
    """Rare Tags"""

    def create(self, request):
        """Handle POST operations
    
        Returns: 
            Response: JSON serialized tag instance
        """

        #Create a new Python instance of the Tags class
        #Set its properties from what was sent in the body
        #Of the request from the client
        tag = Tag()
        tag.label = request.data["label"]

        #Try and save the new tag to the database
        #Then serialize the tag instance as JSON
        #And send the JSON as a response to the client request
        try: 
            tag.save()
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response: Empty body with a 204 status code
        """
        #Similar to POST
        #Instead of creating a new instance of Tag
        #Get the tag record from the database whose primary key is 'pk'
        tag = Tag.objects.get(pk=pk)
        tag.label = request.data["label"]

        #204 status code means everything worked but the
        #server isn't sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single tag

        Returns:
            Response --JSON serialized tag instance
        """
        try:
            # `pk` is a parameter to this function
            # Django parses it from the URL route parameter
            #   http://localhost:8000/tags/2
            # The `2` at the end of the route becomes `pk`
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

    # @action(methods=['post', 'delete'], detail=True)
    # def addTag(self, request, pk=None):
    #     """Managing adding a tag to a post"""

    #     #A user wants to put a tag on a post
    #     if request.method == "POST":
    #         tag = Tag.objects.get(pk=pk)

    #         # Find the post by looking for the pk on the Post
    #         post = Post.objects.get(pk=pk)

    #         try:
    #             #Determine if the tag is already on the post
    #             tagged = PostTag.objects.get(
    #                 tag=tag, post=post)
    #             return Response(
    #                 {'message': 'Tag is already on this post.'},
    #                 status=status.HTTP_422_UNPROCESSABLE_ENTITY
    #             )
    #         except PostTag.DoesNotExist:
    #             #The post doesn't have this tag on it
    #             tagged = PostTag()
    #             tagged.tag = tag
    #             tagged.post = post
    #             tagged.save()

    #             return Response({}, status=status.HTTP_201_CREATED)

    #     # User wants to remove a tag from a post
    #     elif request.method == "DELETE":
    #         #Handle the case if the client
    #         #specifies a tag or post that doesn't exist
    #         try:
    #             tag = Tag.objects.get(pk=pk)
    #         except Tag.DoesNotExist:
    #             return Response(
    #                 {'message': 'Tag does not exist.'},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )
    #         try:
    #             post = Post.objects.get(pk=pk)
    #         except Tag.DoesNotExist:
    #             return Response(
    #                 {'message': 'Post does not exist.'},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )
            
    #         try:
    #             #Try to delete the tag
    #             tagged = PostTag.objects.get(
    #                 tag = tag, post=post)
    #             tagged.delete()
    #             return Response(None, status=status.HTTP_204_NO_CONTENT)

    #         except PostTag.DoesNotExist:
    #             return Response(
    #                 {'message': 'This tag is not currently on this post.'},
    #                 status=status.HTTP_404_NOT_FOUND
    #             )

    #     # If the client performs a request with a method of
    #     # anything other than POST or DELETE, tell client that
    #     # the method is not supported
    #     return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


        
class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags

    Arguments: serializers
    """
    class Meta:
        model = Tag
        fields = ('id', 'label', 'tagged')
