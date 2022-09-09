from django.test import TestCase
import json
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Task
from .serializers import TaskSerializer


class TaskTestCase(APITestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Test Task", completed=False)
        self.task.save()

    def test_task_list(self):
        response = self.client.get(reverse('task-list'))
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_task_list_pagination(self):
        for i in range(1, 100):
            task = Task.objects.create(title="Test Task {}".format(i), completed=False)
            task.save()
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.data['count'], 100)
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.status_code, 200)

    def test_task_create(self):
        response = self.client.post(reverse('task-list'), data={"title": "Test Task 2", "completed": False})
        self.assertEqual(response.status_code, 201)

    def test_task_update(self):
        response = self.client.put(reverse('task-detail', kwargs={'pk': self.task.pk}),
                                   data={"title": "Test Task 2", "completed": True})
        self.assertEqual(response.status_code, 200)

    def test_task_delete(self):
        response = self.client.delete(reverse('task-detail', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 204)

    def test_task_retrieve(self):
        response = self.client.get(reverse('task-detail', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)

    def test_task_partial_update(self):
        response = self.client.patch(reverse('task-detail', kwargs={'pk': self.task.pk}), data={"title": "Test Task 2"})
        self.assertEqual(response.status_code, 200)

    def test_task_not_found(self):
        response = self.client.get(reverse('task-detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_task_not_found_delete(self):
        response = self.client.delete(reverse('task-detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_task_not_found_update(self):
        response = self.client.put(reverse('task-detail', kwargs={'pk': 1000}), data={"title": "Test Task 2", "completed": True})
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        self.task.delete()