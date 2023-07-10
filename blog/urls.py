from django.urls import path
from .views import (
	PostListView, 
	PostDetailView, 
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
	UserPostListView,
	CommentCreateView,
	MessageCreateView,
	AuthorsListView
)
from . import views


urlpatterns = [
path('', PostListView.as_view(), name='blog-home'),
path('post/<int:id>/like', views.like_post, name='post-like'),
path('api/post/<int:id>/like', views.like_unlike_api, name='post-like-unlike-api'),
path('user/<int:id>', views.follow_or_unfollow, name='follow-user'),
path('post/<int:id>/comment', CommentCreateView.as_view(), name='post-comment'),
path('user/<str:username>/posts', UserPostListView.as_view(), name='user-posts'),
path('user/<str:username>', views.user_information, name='user-info'),
path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
path('post/new/', PostCreateView.as_view(), name='post-create'),
path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
path('about/', views.about, name='blog-about'),
path('search',AuthorsListView.as_view() , name="search-user"),
path('message/inbox', MessageCreateView.as_view(), name="message-inbox"),
path('message/<int:id>/inbox', MessageCreateView.as_view(), name="message-user"),
path('api/message/<int:id>', views.get_all_message_api, name="get-message-api"),
path('api/message/<int:id>/create', views.create_message, name="create-message"),
path('api/comment/<int:id>', views.get_all_comments_api, name="get-comments-api"),
path('api/comment/<int:id>/create', views.create_comment, name="create-comment")
]




