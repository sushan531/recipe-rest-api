from user.serializers import UserSerializer
from rest_framework.generics import CreateAPIView

class CreateUserView(CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer
    