from user.serializers import UserSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework import authentication, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication


class CreateUserView(CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(TokenObtainPairView):
    """Create a new auth token for user"""
    pass


class ManageUserView(RetrieveUpdateAPIView):
    """Update user data"""
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
