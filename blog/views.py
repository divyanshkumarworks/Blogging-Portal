from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .forms import CommentForm, MessageForm
from users.models import Profile
from django.http import HttpResponseRedirect
from .models import Post, Comment, UserFollowing, Message
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormMixin
import json
from django.views.generic import (
		ListView, 
		DetailView,
		CreateView,
		UpdateView,
		DeleteView,
		View,
		TemplateView
)
from .models import Post
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.




class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 5


	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView, FormMixin):
	model = Post
	template_name = 'blog/post_detail.html'
	form_class = CommentForm

	
class CommentCreateView(LoginRequiredMixin, CreateView):
	model = Comment
	form_class = CommentForm

	# def form_valid(self, form):
	# 	form.instance.author = self.request.user
	# 	form.instance.post_id = self.kwargs.get('id')
	# 	return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('post-detail', args=[self.kwargs.get('id')])

class MessageCreateView(LoginRequiredMixin, CreateView):
	model = Message
	form_class = MessageForm
	template_name = "blog/message_inbox.html"

	# def form_valid(self, form):
	# 	form.instance.msg_from_user = self.request.user
	# 	form.instance.msg_to_user = User.objects.get(id=self.kwargs.get('id'))
	# 	return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('message-user', args=[self.kwargs.get('id')])

	def get_context_data(self, **kwargs):
		context = super(MessageCreateView, self).get_context_data(**kwargs)
		messages = Message.objects.filter(Q(msg_from_user=self.request.user) | Q(msg_to_user=self.request.user))
		all_unique_user_ids = set(message.msg_to_user.id for message in messages).union(set(message.msg_from_user.id for message in messages))
		try:	
			to_user = User.objects.get(id=self.kwargs.get('id'))
		except User.DoesNotExist:
			to_user = None
		context['users'] = User.objects.filter(id__in=all_unique_user_ids)
		context['dm_messages'] = Message.objects.filter(
			Q(msg_from_user=self.request.user, msg_to_user=to_user)
			| Q(msg_to_user=self.request.user, msg_from_user=to_user) 
			).order_by('created')
		context['to_user'] = to_user
		context['from_user'] = self.request.user
		return context


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True

def like_post(request, id):
	post = Post.objects.get(id=id)
	if request.user in post.likes.all():
		post.likes.remove(request.user)
	else:
		post.likes.add(request.user)
	return redirect(reverse('blog-home') + "?page=" + request.GET['page'] + "#post-" + str(post.id))

def about(request):
	return render(request, 'blog/about.html', {'title': 'About'})


def user_information(request, username):
	user = get_object_or_404(User, username=username)
	followers = UserFollowing.objects.filter(user_to=user).count()
	i_follow = UserFollowing.objects.filter(user_from=user).count()
	following = False

	if request.user.is_authenticated:
		following = UserFollowing.objects.filter(user_to=user, user_from=request.user).exists()

	context = {
		"user": user,
		"following": following,
		"followers": followers,
		"i_follow": i_follow
	}
	return render(request, "blog/public_profile.html", context)


@login_required
def follow_or_unfollow(request, id):
	followed = get_object_or_404(User, id=id)
	followed_by = request.user

	follow, created = UserFollowing.objects.get_or_create(user_to=followed,user_from=followed_by)

	if not created:
		follow.delete()

	return redirect('user-info', username=followed.username)

# def user_search(request):
# 	query = request.GET.get('q')
# 	context = {}
# 	if  query:
# 		users = User.objects.filter(Q(username_icontains=query))
# 		paginator = Paginator(users, 5)
		
# 		page_number = request.GET.get('page')
# 		user_paginator = paginator.get_page(page_number)

# 		context = {
# 		'users': user_paginator
# 		}

# 	return render(request, 'blog/home.html', context)

class AuthorsListView(TemplateView):
	template_name = "blog/user_list.html"

	def get(self, request):
		q = self.request.GET['q']
		results = User.objects.filter(username__icontains=q)
		return render(request, 'blog/user_list.html', {'results': results})
	

@login_required
def like_unlike_api(request, id):
	post = Post.objects.get(id=id)
	if request.user in post.likes.all():
		post.likes.remove(request.user)
		return JsonResponse({"liked": False})
	else:
		post.likes.add(request.user)
		return JsonResponse({"liked": True})

@login_required
def get_all_message_api(request, id):
	try:	
		to_user = User.objects.get(id=id)
	except User.DoesNotExist:
		to_user = None
	
	messages = Message.objects.filter(
		Q(msg_from_user=request.user, msg_to_user=to_user)
		| Q(msg_to_user=request.user, msg_from_user=to_user) 
		).order_by('created')
	
	data = {
		"messages": []
	}
	for message in messages:
		data["messages"].append(
				{
					"id": message.id,
					"text":message.text,
					"name": "You" if request.user == message.msg_from_user else message.msg_from_user.username,
					"profile_pic": message.msg_from_user.profile.image.url,
					"position": "left" if request.user == message.msg_from_user else "right"
				}
			)

	return JsonResponse(data)


@csrf_exempt
@login_required
def create_message(request, id):
	if request.method == 'POST':
		print(request.body)
		data = json.loads(request.body)
		print(data["message"])
		message = Message.objects.create(text=data["message"], msg_from_user=request.user , msg_to_user=User.objects.get(id=data["user_id"]))
		return JsonResponse({"message":"success"})


@csrf_exempt
@login_required
def create_comment(request, id):
	if request.method == 'POST':
		print(request.body)
		data = json.loads(request.body)
		print(data["comment"])
		comment = Comment.objects.create(text=data["comment"], author=request.user, post=Post.objects.get(id=data["post_id"]))
		return JsonResponse({'message':"success"})

def get_all_comments_api(request, id):
	comments = Comment.objects.filter(post_id=id)
	data = {
		"comments": []
	}
	for comment in comments:
		data["comments"].append(
			{
				"commentor": comment.author.username,
				"id": comment.id,
				"date_posted": comment.date_posted,
				"post_id": comment.post.id,
				"text": comment.text,
				"profile_pic": comment.author.profile.image.url
			}
		)

	return JsonResponse(data)

