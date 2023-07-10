from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse 

class Post(models.Model):
	author = models.ForeignKey(User,on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	likes = models.ManyToManyField(User,related_name="likes",blank=True)

	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

class Comment(models.Model):
	text = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="comments")
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

	class Meta:
		ordering = ('-date_posted',)

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk':self.pk})

	def __str__(self):
		return f"{self.author.username} comment on post {self.post.id}" 
	
class UserFollowing(models.Model):
	user_from = models.ForeignKey(User, related_name="user_from_set", on_delete=models.CASCADE)
	user_to = models.ForeignKey(User, related_name="user_to_set", on_delete=models.CASCADE)
	created = models.DateTimeField(default=timezone.now)

	class Meta:
		ordering = ["-created"]
		unique_together = ('user_from', 'user_to',)

	def __str__(self):
		return f"{self.user_from.username} started following {self.user_to.username}"

User.add_to_class('following', models.ManyToManyField('self', through=UserFollowing, related_name='followers', symmetrical=False, blank=True))

class Message(models.Model):
	text = models.TextField()
	msg_from_user = models.ForeignKey(User, related_name="msg_user_from", on_delete=models.CASCADE)
	msg_to_user = models.ForeignKey(User, related_name="msg_user_to", on_delete=models.CASCADE)
	created = models.DateTimeField(default=timezone.now)

	class Meta:
		ordering = ["-created"]

	def __str__(self):
		return f"{self.msg_from_user.username} send a message to {self.msg_to_user.username}"

	def get_absolute_url(self):
		return reverse('message-user', kwargs={'id':self.id})

