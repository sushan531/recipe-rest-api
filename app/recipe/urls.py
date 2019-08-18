from django.urls import path
from recipe.views import TagViewSet, IngredientViewSet


app_name= "recipe"
urlpatterns = [
    path("tag/", TagViewSet.as_view(), name="tag-list"),
    path("ingredient/", IngredientViewSet.as_view(), name="ingredient-list")
]