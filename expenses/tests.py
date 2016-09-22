from django.contrib.auth.models import User, Group

from rest_framework.test import APITestCase
from rest_framework import status


from expenses.models import Expense
from expenses.serializers import ExpenseSerializer


class ItemsAPITestCase(APITestCase):
    list_link = '/expenses/'
    detail_link = '/expenses/{}/'

    def setUp(self):
        self.admin_user = User.objects.create(username='expenses_testing_admin', password='ietaiC2a')
        self.admin_user.groups.add(Group.objects.get(name='admin'))

        self.regular_user = User.objects.create_user(username='expenses_testing_user', password='ohD9Naz4')
        self.regular_user.groups.add(Group.objects.get(name='user'))

        self.user_manager = User.objects.create_user(username='expenses_testing_manager', password='yee1eeGh')
        self.user_manager.groups.add(Group.objects.get(name='user_manager'))

    def test_regular_user_expenses_list(self):
        self.client.force_login(self.regular_user)
        Expense.objects.create(user=self.regular_user, text='teV1mu0r', cost=6)

        actual_users_expenses = ExpenseSerializer(self.regular_user.expense_set.all(), many=True).data
        response = self.client.get(self.list_link)

        self.assertEqual(response.json(), actual_users_expenses)

    def test_admin_user_expenses_list(self):
        self.client.force_login(self.admin_user)
        Expense.objects.create(user=self.admin_user, text='pohNg0ei', cost=6)

        actual_users_expenses = ExpenseSerializer(Expense.objects.all(), many=True).data
        response = self.client.get(self.list_link)

        self.assertEqual(response.json(), actual_users_expenses)

    def test_manager_permission(self):
        self.client.force_login(self.user_manager)
        self.assertEqual(self.client.get(self.list_link).status_code, status.HTTP_403_FORBIDDEN)

    def test_expense_create(self):
        self.client.force_login(self.regular_user)
        response = self.client.post(self.list_link, {'user': self.regular_user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_expense_create(self):
        self.client.force_login(self.regular_user)
        response = self.client.post(self.list_link, {"cost": "cai4reiZ"})
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_regular_user_attempts_to_create_expense_for_others(self):
        self.client.force_login(self.regular_user)
        response = self.client.post(self.list_link, {'user': self.admin_user.id})
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_admin_user_attempts_to_create_expense_for_others(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(self.list_link, {'user': self.regular_user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_expense_update(self):
        self.client.force_login(self.regular_user)
        item_data = self.client.post(self.list_link, {'user': self.regular_user.id}).json()
        item_data['text'] = 'testing_item'
        response = self.client.patch(
            self.detail_link.format(item_data['id']), item_data, format='json')
        self.assertEqual(response.json(), item_data)

    def test_regular_user_attempts_to_update_others_expense(self):
        self.client.force_login(self.admin_user)
        item_data = self.client.post(self.list_link, {'user': self.admin_user.id}).json()

        self.client.force_login(self.regular_user)
        item_data['text'] = 'testing_item'
        response = self.client.patch(
            self.detail_link.format(item_data['id']), item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_user_attempts_to_update_others_expense(self):
        self.client.force_login(self.regular_user)
        item_data = self.client.post(self.list_link, {'user': self.regular_user.id}).json()

        self.client.force_login(self.admin_user)
        item_data['text'] = 'testing_item'
        response = self.client.patch(
            self.detail_link.format(item_data['id']), item_data, format='json')
        self.assertEqual(response.json(), item_data)

    def test_expense_remove(self):
        self.client.force_login(self.regular_user)
        item_data = self.client.post(
            self.list_link, {'text': 'bread', 'cost': 10, 'user': self.regular_user.id}).json()
        response = self.client.delete(
            self.detail_link.format(item_data['id']))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_attempts_to_remove_others_expense(self):
        self.client.force_login(self.admin_user)

        expense = Expense.objects.create(user=self.regular_user, text='food', cost=66)
        response = self.client.delete(self.detail_link.format(expense.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_regular_user_attempts_to_remove_others_expense(self):
        self.client.force_login(self.regular_user)
        expense = Expense.objects.create(user=self.admin_user, text='fish', cost=666)

        response = self.client.delete(self.detail_link.format(expense.id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UsersAPITestCase(APITestCase):
    list_link = '/users/'
    detail_link = '/users/{}/'

    def setUp(self):
        self.admin_user = User.objects.create(username='users_testing_admin', password='ietaiC2a')
        self.admin_user.groups.add(Group.objects.get(name='admin'))

        self.regular_user = User.objects.create_user(username='users_testing_user', password='ohD9Naz4')
        self.regular_user.groups.add(Group.objects.get(name='user'))

        self.user_manager = User.objects.create_user(username='users_testing_manager', password='yee1eeGh')
        self.user_manager.groups.add(Group.objects.get(name='user_manager'))

    def test_create_user(self):
        self.client.force_login(self.user_manager)
        response = self.client.post(
            self.list_link, {'username': 'cat', 'password': 123}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        self.client.force_login(self.user_manager)
        response = self.client.post(
            self.list_link, {'username': 111, 'password': False}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_sets_user_group(self):
        self.client.force_login(self.user_manager)
        response = self.client.post(
            self.list_link, {'username': 'ev0ieGe7', 'password': 123}, format='json')

        created_user = User.objects.get(id=response.json()['id'])
        self.assertTrue(created_user.groups.filter(name='user').exists())

    def test_patch_user(self):
        self.client.force_login(self.user_manager)
        user_data = self.client.post(
            self.list_link, {'username': 'dog', 'password': 123}, format='json').json()
        user_data['username'] = 'dog1'
        response = self.client.put(
            self.detail_link.format(user_data['id']), user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_attempts_to_update_admin_user(self):
        another_admin_user = User.objects.create(username='updated_users_testing_admin', password='ietaiC2a')
        another_admin_user.groups.add(Group.objects.get(name='admin'))

        self.client.force_login(self.user_manager)
        response = self.client.patch(
            self.detail_link.format(another_admin_user.id),
            {"username": "patched_users_testing_admin"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_manager_attempts_to_update_another_manager_user(self):
        another_manager_user = User.objects.create(username='updated_users_testing_manager', password='ietaiC2a')
        another_manager_user.groups.add(Group.objects.get(name='user_manager'))

        self.client.force_login(self.user_manager)
        response = self.client.patch(
            self.detail_link.format(another_manager_user.id),
            {"username": "patched_users_testing_manager"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user(self):
        self.client.force_login(self.user_manager)
        user_data = self.client.post(
            self.list_link, {'username': 'dog1', 'password': 123}, format='json').json()
        response = self.client.delete(
            self.detail_link.format(user_data['id']))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_manager_attempts_to_delete_admin_user(self):
        another_admin_user = User.objects.create(username='deleted_users_testing_admin', password='ietaiC2a')
        another_admin_user.groups.add(Group.objects.get(name='admin'))

        self.client.force_login(self.user_manager)
        response = self.client.delete(
            self.detail_link.format(another_admin_user.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_manager_attempts_to_delete_manager_user(self):
        another_manager_user = User.objects.create(username='deleted_users_testing_manager', password='ietaiC2a')
        another_manager_user.groups.add(Group.objects.get(name='user_manager'))

        self.client.force_login(self.user_manager)
        response = self.client.delete(
            self.detail_link.format(another_manager_user.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)