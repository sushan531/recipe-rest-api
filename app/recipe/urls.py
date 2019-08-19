from django.urls import path
from recipe.views import TagViewSet, IngredientViewSet, RecipeViewSet


app_name= "recipe"
urlpatterns = [
    path("tag/", TagViewSet.as_view(), name="tag-list"),
    path("ingredient/", IngredientViewSet.as_view(), name="ingredient-list"),
    path("recipes/", RecipeViewSet.as_view({"get":"list"}), name="recipe-list"),
    path("recipes/create/", RecipeViewSet.as_view({"post": "create"}), name="recipe-create"),
    path("recipes/<int:pk>/", RecipeViewSet.as_view({"get": "retrieve"}), name="recipe-detail"),

]