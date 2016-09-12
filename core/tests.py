from django.contrib.auth.models import User, Group

from rest_framework.test import APIClient, APITestCase
from rest_framework import status


class ItemsAPITestCase(APITestCase):
    list_link = '/core/items/'
    detail_link = '/core/item/{}/'

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testing_admin', password='123123')
        self.client.force_login(self.user)

    def test_items_create(self):
        response = self.client.post(self.list_link)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_item_update(self):
        item_data = self.client.post(self.list_link).json()
        item_data['text'] = 'testing_item'
        response = self.client.patch(
            self.detail_link.format(item_data['id']), item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_item_delete(self):
        item_data = self.client.post(self.list_link).json()
        response = self.client.delete(
            self.detail_link.format(item_data['id']))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UsersAPITestCase(APITestCase):
    list_link = '/core/users/'
    detail_link = '/core/user/{}/'

    def setUp(self):
        self.client = APIClient()
        self.manager_user = User.objects.create(username='testing_user_manager', password='123123')
        manager_group = Group.objects.get(name='user_manager')
        self.manager_user.groups.add(manager_group)
        self.client.force_login(self.manager_user)

    def test_create_user(self):
        response = self.client.post(
            self.list_link, {'username': 'cat', 'password': 123}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_user(self):
        user_data = self.client.post(
            self.list_link, {'username': 'dog', 'password': 123}, format='json').json()
        user_data['username'] = 'dog1'
        response = self.client.put(
            self.detail_link.format(user_data['id']), user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_item_delete(self):
        user_data = self.client.post(
            self.list_link, {'username': 'dog1', 'password': 123}, format='json').json()
        response = self.client.delete(
            self.detail_link.format(user_data['id']))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
