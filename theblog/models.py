from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name
		
	def get_absolute_url(self):
		return reverse('home')

class Post(models.Model):
	title = models.CharField(max_length = 255) # Title Field
	author = models.ForeignKey(User, on_delete = models.CASCADE) # Deletes blog posts for a user if they delete account
	header_image = models.ImageField(null = True, blank = True, upload_to = 'uploads/images', default = None)
	#body = models.TextField()
	body = RichTextField(blank= True, null = True)
	date_published = models.DateTimeField(auto_now_add = True) # Automatically adds the date
	likes = models.ManyToManyField(User, related_name ='blog_post') # Updating count of the upvotes 
	tags = models.CharField(max_length = 255, default = 'Coding') # List of tags from the Tag table	
	snippet  = models.CharField(max_length = 300, default = 'Article Snippet') # Article Snippet field to display on screen
	#header_image = models.ImageField(blank = True, null = True, upload_to = 'images/') # Stores the file location of header image
	number_likes = models.IntegerField(default = 0)
	def __str__(self):
		return self.title + ' | ' + str(self.author) # Return 'title|author' to display on home page
	
	def get_absolute_url(self):
		return reverse('home')

	def total_like_count(self):
		return self.likes.count()


class Comment(models.Model):
	post = models.ForeignKey(Post,related_name = 'comments', on_delete = models.CASCADE)
	name = models.CharField(max_length = 255)
	body = models.CharField (max_length = 255)
	date_added = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return '%s - %s' % (self.post.title, self.name)


class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key= True, verbose_name = 'user', related_name = 'profile', on_delete = models.CASCADE)
	name = models.CharField(max_length = 30, blank = True, null = True)
	bio = models.TextField(max_length=500, blank = True, null = True)
	birthday = models.DateField(null = True, blank = True)
	location = models.CharField(max_length = 100, blank = True, null = True)
	picture = models.ImageField(upload_to = 'uploads/profile_pictures', default = 'uploads/profile_pictures/default.png', blank = True)
	followers = models.ManyToManyField(User, blank = True, related_name = 'followers')
	notification  = models.BooleanField(default = True, blank = False, null = False)
	follower_count = models.IntegerField(null = True, default = 0)
	website = models.CharField(default = None, blank = True, null = True, max_length = 50)
	GitHub = models.CharField(default = None, blank = True, null = True, max_length = 50)
	Twitter = models.CharField(default = None, blank = True, null = True, max_length = 50)
	Instagram = models.CharField(default = None, blank = True, null = True, max_length = 50)
	FaceBook = models.CharField(default = None, blank = True, null = True, max_length = 50)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance) 

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()