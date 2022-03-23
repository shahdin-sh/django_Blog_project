from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
from django.shortcuts import reverse


class PostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='sample1')
        cls.post = Post.objects.create(
            title='sample_post',
            text='sample_text',
            status=Post.STATUS_CHOICES[0][0],
            author=cls.user
        )
        cls.post2 = Post.objects.create(
            title='sample_post2',
            text='sample_text2',
            status=Post.STATUS_CHOICES[0][1],
            author=cls.user

        )

    def test_post_list_url(self):
        response = self.client.get('/blog/')
        self.assertEquals(response.status_code, 200)

    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('post_view_of_blog'))
        self.assertEquals(response.status_code, 200)

    def test_post_blog_title_on_list_page(self):
        response = self.client.get(reverse('post_view_of_blog'))
        self.assertContains(response, self.post.title)

    def test_post_detail_url_by_name(self):
        response = self.client.get(reverse('post_detail_view', args=[self.post.id]))
        self.assertEquals(response.status_code, 200)

    def test_post_blog_on_details_page(self):
        response = self.client.get(f'/blog/{self.post.id}')
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.text)

    def if_post_does_not_exit_404_error_handling(self):
        response = self.client.get(reverse('post_detail_view', args=[9999+1]))
        self.assertEquals(response.status_code, 404)

    def test_draft_post_not_show_in_post_list(self):
        response = self.client.get(reverse('post_view_of_blog'))
        self.assertNotContains(response, self.post2.title)

    def test_title_str(self):
        post = self.post
        self.assertEquals(str(post), post.title)

    def test_post_detail(self):
        post = self.post
        self.assertEquals(self.post.title, 'sample_post')
        self.assertEquals(self.post.text, 'sample_text')
        self.assertEquals(self.post.status, Post.STATUS_CHOICES[0][0])

    def test_post_creat_view(self):
        response = self.client.post(reverse('post_view_add'), {
            'title': 'something',
            'text': 'text_something',
            'status': 'pub',
            'user': self.user.id,
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.last().title, 'something'),
        self.assertEquals(Post.objects.last().text, 'text_something')

    def test_post_edit_option(self):
        # problem with this  test
        response = self.client.post(reverse('post_edit_option', args=[self.post2.id]), {
            'title': 'sample_title2_updated',
            'text': 'sample_text2_updated',
            'status': 'pub',
            'user': self.post2.author.id,
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.last().title, 'sample_title2_updated'),
        self.assertEquals(Post.objects.last().text, 'sample_text2_updated')

    def test_post_delete_option(self):
        response = self.client.post(reverse('post_delete_option', args=[self.post2.id]))
        self.assertEquals(response.status_code, 302)




