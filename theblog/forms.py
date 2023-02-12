from django import forms
from .models import Post, Category, Comment, UserProfile


choices = Category.objects.all().values_list('name','name')

choice_list = []
for element in choices:
	choice_list.append(element)

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title','author', 'tags','body','snippet', 'header_image') # Fields to be displayed on add 
		# article page
		widgets ={
			'title':forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Title...'}), # title field is a text input 
			'author':forms.TextInput(attrs = {'class':'form-control', 'value':'', 'id':'user_label', 'type':'hidden'}), # Author
			# assigned automatically
			'tags': forms.Select(choices = choices, attrs = {'class':'form-control'}),
			#'tags':forms.Select(choices = choice_list, attrs = {'class':'form-control'}), # Tags is a dropdown selection bar
			'body':forms.Textarea(attrs ={'class':'form-control', 'placeholder':'Start Writing...'}), # Article is written here
			'snippet':forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Snippet...'}) # Snippet is written here
		}

class UpdateForm(forms.ModelForm):
	class Meta:
		model = Post 
		#fields = ['title','title_tag','body','snippet']
		fields = ('title', 'body','snippet', 'header_image')

		widgets = {
			'title':forms.TextInput(attrs = {'class':'form-control'}),
			#'tags':forms.Select(choices = choice_list, attrs = {'class':'form-control'}),
			'body':forms.Textarea(attrs = {'class':'form-control'}),
			'snippet':forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Snippet...'}),
		}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment

		fields = ['name', 'body']
		widgets = {
			'name':forms.TextInput(attrs = {'class':'form-control'}),
			'body':forms.Textarea(attrs = {'class':'form-control'})

		}

