from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from newspaper_agency.models import Topic, Redactor, Newspaper

class TestViews(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.redactor = Redactor.objects.create(user=self.user, first_name="Test", last_name="Redactor", years_of_experience=5)
        self.topic = Topic.objects.create(name="Test Topic")
        self.newspaper = Newspaper.objects.create(title="Test Newspaper", content="Test Content", published_date="2024-12-12")
        self.newspaper.topics.add(self.topic)
        self.newspaper.publishers.add(self.redactor)

    def test_base_view(self):
        response = self.client.get(reverse("newspaper_agency:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/index.html")
        self.assertContains(response, "num_topics")
        self.assertContains(response, "num_redactors")
        self.assertContains(response, "num_newspapers")

    def test_register_view(self):
        response = self.client.get(reverse("newspaper_agency:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

        form_data = {
            "username": "newredactor",
            "password": "newpassword",
            "first_name": "New",
            "last_name": "Redactor",
            "years_of_experience": 3,
        }
        response = self.client.post(reverse("newspaper_agency:register"), data=form_data)
        self.assertRedirects(response, reverse("newspaper_agency:login"))
        self.assertTrue(Redactor.objects.filter(username="newredactor").exists())

    def test_login_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("newspaper_agency:index"))
        self.assertEqual(response.status_code, 200)

    def test_topic_list_view(self):
        response = self.client.get(reverse("newspaper_agency:topic_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/topic_list.html")
        self.assertContains(response, self.topic.name)

    def test_topic_create_view(self):
        response = self.client.get(reverse("newspaper_agency:topic_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/topic_form.html")

        form_data = {"name": "New Topic"}
        response = self.client.post(reverse("newspaper_agency:topic_create"), data=form_data)
        self.assertRedirects(response, reverse("newspaper_agency:topic_list"))
        self.assertTrue(Topic.objects.filter(name="New Topic").exists())

    def test_topic_update_view(self):
        response = self.client.get(reverse("newspaper_agency:topic_update", kwargs={"pk": self.topic.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/topic_update.html")

        form_data = {"name": "Updated Topic"}
        response = self.client.post(reverse("newspaper_agency:topic_update", kwargs={"pk": self.topic.pk}), data=form_data)
        self.assertRedirects(response, reverse("newspaper_agency:topic_list"))
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.name, "Updated Topic")

    def test_topic_delete_view(self):
        response = self.client.get(reverse("newspaper_agency:topic_delete", kwargs={"pk": self.topic.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/topic_delete.html")

        response = self.client.post(reverse("newspaper_agency:topic_delete", kwargs={"pk": self.topic.pk}))
        self.assertRedirects(response, reverse("newspaper_agency:topic_list"))
        self.assertFalse(Topic.objects.filter(pk=self.topic.pk).exists())

    def test_newspaper_list_view(self):
        response = self.client.get(reverse("newspaper_agency:newspaper_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/newspaper_list.html")
        self.assertContains(response, self.newspaper.title)

    def test_newspaper_detail_view(self):
        response = self.client.get(reverse("newspaper_agency:newspaper_detail", kwargs={"pk": self.newspaper.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/newspaper_detail.html")
        self.assertContains(response, self.newspaper.title)

    def test_newspaper_form_view(self):
        response = self.client.get(reverse("newspaper_agency:newspaper_form"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/newspaper_form.html")

        form_data = {
            "title": "New Newspaper",
            "content": "New Content",
            "published_date": "2024-12-12",
            "topics": [self.topic.pk],
            "publishers": self.redactor.pk,
        }
        response = self.client.post(reverse("newspaper_agency:newspaper_form"), data=form_data)
        self.assertRedirects(response, reverse("newspaper_agency:newspaper_list"))
        self.assertTrue(Newspaper.objects.filter(title="New Newspaper").exists())

    def test_newspaper_update_view(self):
        response = self.client.get(reverse("newspaper_agency:newspaper_update", kwargs={"pk": self.newspaper.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/newspaper_update.html")

        form_data = {"title": "Updated Newspaper"}
        response = self.client.post(reverse("newspaper_agency:newspaper_update", kwargs={"pk": self.newspaper.pk}), data=form_data)
        self.assertRedirects(response, reverse("newspaper_agency:newspaper_detail", kwargs={"pk": self.newspaper.pk}))
        self.newspaper.refresh_from_db()
        self.assertEqual(self.newspaper.title, "Updated Newspaper")

    def test_newspaper_delete_view(self):
        response = self.client.get(reverse("newspaper_agency:newspaper_delete", kwargs={"pk": self.newspaper.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/newspaper_delete.html")

        response = self.client.post(reverse("newspaper_agency:newspaper_delete", kwargs={"pk": self.newspaper.pk}))
        self.assertRedirects(response, reverse("newspaper_agency:newspaper_list"))
        self.assertFalse(Newspaper.objects.filter(pk=self.newspaper.pk).exists())
