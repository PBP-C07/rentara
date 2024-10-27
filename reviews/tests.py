from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from reviews.models import Reviews
from reviews.forms import ReviewsForm

class ReviewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create_review(self):
        response = self.client.post(reverse('reviews:create_reviews'), {
            'title': 'Test Review',
            'rating': 5,
            'description': 'This is a test review.'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Reviews.objects.count(), 1)
        self.assertEqual(Reviews.objects.first().title, 'Test Review')

    def test_edit_review(self):
        review = Reviews.objects.create(
            title='Original Title',
            user=self.user,
            rating=4,
            description='Original description.'
        )
        
        response = self.client.post(reverse('reviews:edit_review', args=[review.id]), {
            'title': 'Edited Title',
            'rating': 5,
            'description': 'Edited description.'
        })
        self.assertEqual(response.status_code, 302) 
        review.refresh_from_db()
        self.assertEqual(review.title, 'Edited Title')

    def test_delete_review(self):
        review = Reviews.objects.create(
            title='Review to be deleted',
            user=self.user,
            rating=3,
            description='This review will be deleted.'
        )
        
        response = self.client.post(reverse('reviews:delete_review', args=[review.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reviews.objects.count(), 0)  # Review should be deleted

    def test_show_reviews(self):
        # Create a review
        Reviews.objects.create(
            title='Sample Review',
            user=self.user,
            rating=5,
            description='This is a sample review.'
        )
        response = self.client.get(reverse('reviews:show_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sample Review')

    def test_show_json(self):
        # Create a review
        Reviews.objects.create(
            title='JSON Review',
            user=self.user,
            rating=5,
            description='This is a review for JSON response.'
        )
        response = self.client.get(reverse('reviews:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_xml(self):
        # Create a review
        Reviews.objects.create(
            title='XML Review',
            user=self.user,
            rating=5,
            description='This is a review for XML response.'
        )
        response = self.client.get(reverse('reviews:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def tearDown(self):
        self.user.delete()
        Reviews.objects.all().delete()