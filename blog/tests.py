from django.test import TestCase
from .models import Post
from django.contrib.auth.models import User
from django.shortcuts import reverse


class BlogPostTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create(
			username = 'user1',
		)
		
		cls.post1 = Post.objects.create(
			title = 'post1',
			text = 'test description 01',
			status = Post.STATUS_CHOICES[0][0],
			author = cls.user
		)
		
		cls.post2 = Post.objects.create(
			title = 'post2',
			text = 'test description 02',
			status = Post.STATUS_CHOICES[1][0],
			author = cls.user
		)
	
	def test_model_string(self):
		self.assertEqual(str(self.post1), self.post1.title)
	
	def test_post_list_url(self):
		response = self.client.get('/blog/')
		self.assertEqual(response.status_code, 200)
	
	def test_post_detail(self):
		self.assertEqual(self.post1.title, 'post1')
		self.assertEqual(self.post1.text, 'test description 01')
	
	def test_post_list_view_by_name(self):
		response = self.client.get(reverse('post_list'))
		self.assertEqual(response.status_code, 200)
	
	def test_post_detail_page_url(self):
		response = self.client.get(f'/blog/{self.post1.id}/')
		self.assertEqual(response.status_code, 200)
	
	def test_detail_page_by_name(self):
		response = self.client.get(reverse('post_detail', args = [self.post1.id]))
		self.assertEqual(response.status_code, 200)
	
	def test_post_title_blog_list_page(self):
		response = self.client.get(reverse('post_list'))
		self.assertContains(response, self.post1.title)
	
	def test_post_detail_on_detail_blog_page(self):
		response = self.client.get(f'/blog/{self.post1.id}/')
		self.assertContains(response, self.post1.title)
		self.assertContains(response, self.post1.text)
	
	def test_draft_post_not_show_in_blog_list(self):
		response = self.client.get("/blog/")
		self.assertContains(response, self.post1.title)
		self.assertNotContains(response, self.post2.title)
	
	def test_post_create_view(self):
		response = self.client.post(reverse('add_post'), {
			'title': 'test post',
			'text': 'test text',
			'status': 'pub',
			'author': self.user.id,
		})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Post.objects.last().title, 'test post')
		self.assertEqual(Post.objects.last().text, 'test text')
	
	def test_post_update_view(self):
		response = self.client.post(reverse('update_post', args = [self.post2.id]), {
			'title': 'post title 01',
			'text': 'post description 1',
			'status': 'pub',
			'author': self.post2.author.id,
		})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Post.objects.last().title, 'post title 01')
		self.assertEqual(Post.objects.last().text, 'post description 1')
	
	def test_post_delete_view(self):
		response = self.client.post(reverse('delete_post', args = [self.post2.id]))
		self.assertEqual(response.status_code, 302)
		