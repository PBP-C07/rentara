from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from reviews.models import Reviews
from reviews.forms import ReviewsForm

class ReviewsTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create_review_invalid_data(self):
        response = self.client.post(reverse('reviews:create_reviews'), {
            'title': '',
            'rating': 6,
            'description': 'This is a test review.'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Reviews.objects.count(), 0)

    def test_edit_nonexistent_review(self):
        response = self.client.post(reverse('reviews:edit_review', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_review(self):
        response = self.client.post(reverse('reviews:delete_review', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_show_reviews_empty(self):
        response = self.client.get(reverse('reviews:show_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No reviews found')

    def test_create_review_without_login(self):
        self.client.logout()
        response = self.client.post(reverse('reviews:create_reviews'), {
            'title': 'Test Review',
            'rating': 5,
            'description': 'This is a test review.'
        })
        self.assertEqual(response.status_code, 403)

    def test_edit_review_permission(self):
        another_user = User.objects.create_user(username='anotheruser', password='12345')
        review = Reviews.objects.create(
            title='Review by Test User',
            user=self.user,
            rating=4,
            description='Original description.'
        )
        self.client.login(username='anotheruser', password='12345')
        response = self.client.post(reverse('reviews:edit_review', args=[review.id]), {
            'title': 'Malicious Edit',
            'rating': 5,
            'description': 'Trying to edit another user\'s review.'
        })
        self.assertEqual(response.status_code, 403)

    def test_create_review_with_long_title(self):
        long_title = 'A' * 256
        response = self.client.post(reverse('reviews:create_reviews'), {
            'title': long_title,
            'rating': 5,
            'description': 'This is a test review.'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Reviews.objects.count(), 0)

    def test_show_reviews_pagination(self):
        for i in range(15):
            Reviews.objects.create(
                title=f'Review {i}',
                user=self.user,
                rating=5,
                description=f'This is review number {i}.'
            )
        response = self.client.get(reverse('reviews:show_reviews') + '?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Review 0')
        self.assertContains(response, 'Review 14')
        self.assertNotContains(response, 'Review 15')

    def test_json_response_format(self):
        Reviews.objects.create(
            title='JSON Format Review',
            user=self.user,
            rating=5,
            description='This review checks JSON format.'
        )
        response = self.client.get(reverse('reviews:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        json_response = response.json()
        self.assertIsInstance(json_response, list)
        self.assertGreater(len(json_response), 0)

    def test_xml_response_format(self):
        Reviews.objects.create(
            title='XML Format Review',
            user=self.user,
            rating=5,
            description='This review checks XML format.'
        )
        response = self.client.get(reverse('reviews:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertContains(response, '<reviews>')