# view model for handling GAME requests
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Comment, Post, RareUser

class Comments(ViewSet):
        # handle POST operations, returns JSON serialized GAME INSTANCE
    def create(self, request):
        # use token passed in the 'Authorization' header
        post = Post.objects.get(pk=request.data["post_id"])
        author = RareUser.objects.get(user = request.auth.user)
        # create a new Python instance of the Comment class con properties de REQUEST de client 
        comment = Comment()
        comment.content = request.data["content"]
        comment.created_on = request.data["created_on"]
        comment.post_id = post.id
        # now use the Djanog ORM to fetch the record from the database whose 'id' is what the client passed as commentTypeId
        comment.author_id = author.id

        # try to save the new comment to the db, then serialize it to JSON, then send that JSON back to client
        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk = None):
    #handle GET request for single comment, returns JSON serialized GAME INSTANCE
        try:
            # 'pk' is a parameter for this function, Django parses it from the URL, ie comments/2, pk=2
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def update(self, request, pk = None):
        # handle PUT request for comments, response: empty body with 204 status code
        # use token passed in the 'Authorization' header
        post = Post.objects.get(pk=request.data["post_id"])
        author = RareUser.objects.get(user = request.auth.user)
        # create a new Python instance of the Comment class con properties de REQUEST de client 
        comment = Comment()
        comment.content = request.data["content"]
        comment.created_on = request.data["created_on"]
        comment.post_id = post.id
        # now use the Djanog ORM to fetch the record from the database whose 'id' is what the client passed as commentTypeId
        comment.author_id = author.id
        
        comment.save()
        # 204 status send back
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        #Handle DELETE requests/ single comment, returns 200, 404, or 500 status code
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        # handle GET all comments, returns JSON serialized list of comments
        comments = Comment.objects.all()
        # ORM command to get all comment records from db
        comment_type = self.request.query_params.get('type', None)
        # we can check to filter the comments by type in a query string ie: comments?type=1 would return all board comments
        if comment_type is not None:
            comments = comments.filter(comment_type__id=comment_type)
        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)


# JSON serializer for comments, argument: serializer type
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','post_id', 'author_id', 'content','created_on')
        depth = 1