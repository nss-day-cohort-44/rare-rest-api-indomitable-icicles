# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
# from django.http import HttpResponseServerError
# from rest_framework import status
# from rest_framework.decorators import action
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import serializers
# from levelupapi.models import Post
# from levelupapi.views.post import GameSerializer

#  def retrieve(self, request, pk=None):
#       """Handle GET requests for single game
#         Returns:
#             Response -- JSON serialized game instance
#         """
#        try:
#             # `pk` is a parameter to this function, and
#             # Django parses it from the URL route parameter
#             #   http://localhost:8000/games/2
#             #
#             # The `2` at the end of the route becomes `pk`
#             post = Post.objects.get(pk=pk)
#             serializer = PostSerializer(post, context={'request': request})
#             return Response(serializer.data)
#         except Exception as ex:
#             return HttpResponseServerError(ex)

# def list(self, request):
#         """Handle GET requests to games resource
#         Returns:
#             Response -- JSON serialized list of games
#         """
#         # Get all game records from the database
#         posts = Post.objects.all()

#         # Support filtering games by type
#         #    http://localhost:8000/games?type=1
#         #
#         # That URL will retrieve all tabletop games
#         game_type = self.request.query_params.get('type', None)
#         if game_type is not None:
#             games = games.filter(gametype__id=game_type)

#         serializer = GameSerializer(
#             games, many=True, context={'request': request})
#         return Response(serializer.data)

# class GameSerializer(serializers.ModelSerializer):
#     """JSON serializer for posts
#     Arguments:
#         serializer type
#     """
#     class Meta:
#         model = Post
#         fields = ('id', 'title', 'maker', 'number_of_players',
#                   'skill_level', 'game_type')
#         depth = 1
