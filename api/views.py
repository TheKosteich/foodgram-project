from rest_framework import viewsets


from api.serializers import IngredientSerializer
from recipes.models import Ingredient


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
