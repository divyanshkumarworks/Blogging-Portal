from django import forms
from .models import Comment, Message

class CommentForm(forms.ModelForm):
	text = forms.CharField(label ="", widget=forms.Textarea(
		attrs ={
			'class': 'form-control',
			'placeholder': 'Say Something...',
			'rows': 2,
			'cols': 30
		}))

	class Meta:
		model = Comment
		fields = ['text']

class MessageForm(forms.ModelForm):
	text = forms.CharField(label ="", widget=forms.Textarea(
		attrs ={
			'class': 'form-control',
			'placeholder': 'type your message',
			'rows': 1,
			'cols': 52
		}))

	class Meta:
		model = Message
		fields = ['text']
		

	