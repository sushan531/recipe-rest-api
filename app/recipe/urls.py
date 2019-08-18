from django.urls import path
from recipe.views import TagViewSet


app_name= "recipe"
urlpatterns = [
    path("", TagViewSet.as_view(), name="tag-list")
]