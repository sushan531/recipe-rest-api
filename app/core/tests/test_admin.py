from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        # Creating user
        self.admin_user = get_user_model().objects.create_superuser(
            username="kasper",
            email="kasper@gmail.com",
            password="Admin@123",
        )

        # login using super user
        self.client.force_login(self.admin_user)

        # creating normal user
        self.user = get_user_model().objects.create_user(
            username="test1",
            email="test1@gmail.com",
            password="test1@123",
        )

    def test_user_changelist(self):
        """Test that users are listed in user page."""
        url = reverse_lazy('admin:core_customuser_changelist')
        response = self.client.get(url)
        self.assertContains(response, self.user.username)

    def test_user_change(self):
        """Test user edit page works"""
        url = reverse_lazy('admin:core_customuser_change', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """test user create page works"""
        url = reverse_lazy("admin:core_customuser_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
