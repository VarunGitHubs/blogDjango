from django.shortcuts import render, get_object_or_404, redirect 
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Category, Comment, UserProfile
from .forms import PostForm, UpdateForm, CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class HomeView(ListView):
	ordering = ['-id']
	model = Post
	template_name = 'home.html'


	def get_context_data(self,*args, **kwargs):
		article_information = Post.objects.all().order_by('-number_likes')
		top_six = article_information[:6]
		tag_menu = Category.objects.all()

		author_information = UserProfile.objects.all().order_by('-follower_count')
		is_following = False
		for author in author_information:
			profile = UserProfile.objects.get(pk = author.pk)
			num_followers = profile.follower_count
			is_following = False


		context = super(HomeView, self).get_context_data(*args, **kwargs)		
		context['tag_menu'] = tag_menu
		context['top_posts'] = top_six
		context['top_authors'] = author_information
		#context['is_following'] = is_following
		return context

class ArticleDetailView(DetailView):
	model = Post
	template_name = 'article_details.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
		article_information = get_object_or_404(Post, id = self.kwargs['pk'])
		total_likes = article_information.total_like_count()
		tag_menu = Category.objects.all()
		context['total_likes'] = total_likes
		context['tag_menu'] = tag_menu
		return context

class ArticlePostView(CreateView):
	model = Post
	form_class = PostForm
	template_name = "add_article.html"

	#def post(self, request, pk, *args, **kwargs):


class AddCommentView(CreateView):
	model = Comment
	form_class = CommentForm
	template_name = "add_comment.html"

	def form_valid(self, form):
		form.instance.post_id = self.kwargs['pk']
		return super().form_valid(form)
	 
	success_url = reverse_lazy('home')


class UpdatePostView(UpdateView):
	model = Post
	form_class = UpdateForm
	template_name = 'update_post.html'

def LikePostView(request, pk):
	post = get_object_or_404(Post, id = request.POST.get('post_id'))
	post.likes.add(request.user)
	post.number_likes += 1
	post.save()
	return HttpResponseRedirect(reverse('article-detail', args = [str(pk)]))

class AddCategoryView(CreateView):
	model = Category
	template_name = 'add_category.html'
	fields = '__all__'

def CategoryView(request, cats):
	cat_posts = Post.objects.filter(tags = cats)
	return render (request, 'categories.html', {'cats':cats.title(), 'cat_posts':cat_posts})

def CategoryListView(request):
	cat_menu_list = Category.objects.all()
	return render(request, 'category_list.html', {'cat_menu_list':cat_menu_list})

class ProfileView(View):
	def get(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk = pk)
		user = profile.user
		posts = Post.objects.filter(author = user).order_by('-date_published')
		followers = profile.followers.all()


		is_following = False


		num_followers = len(followers)
		if num_followers == 0:
			is_following = False
		else:
			for follower in followers:
				if follower == request.user:
					is_following = True 
		context = {
			'user':user,
			'profile':profile,
			'posts':posts,
			'num_followers':num_followers,
			'is_following':is_following
		}

		return render(request, 'user_profile.html', context)



# class ProfileView(DetailView):
# 	model = UserProfile
# 	template_name = 'user_profile.html'

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(ProfileView, self).get_context_data(*args, **kwargs)
# 		userInformation = get_object_or_404(UserProfile, id = self.kwargs(['pk']))
# 		user = userInformation.user 
# 		posts = Post.objects.filter(author = user).order_by('-date_published')
# 		num_followers = userInformation(follower_count)
# 		followers = userInformation.followers.all()

# 		is_following = False

# 		if num_followers == 0:
# 			is_following = False 
# 		else:
# 			is_following = [request.user  ==]


# 		context['total_likes'] = total_likes
# 		context['tag_menu'] = tag_menu
# 		return context




class UserProfileUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
	model = UserProfile
	fields = ['name', 'bio','birthday','location', 'picture']
	template_name = 'profile_edit.html'

	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse_lazy('profile', kwargs = {'pk': pk})
	

	def test_func(self):
		profile = self.get_object()
		return self.request.user == profile.user

class AddFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk = pk)
		profile.followers.add(request.user)

		profile.follower_count += 1
		profile.save()

		return redirect('profile', pk = profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
	def post (self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk = pk)
		profile.followers.remove(request.user)
		profile.num_followers -= 1
		profile.save()
		return redirect('profile', pk=profile.pk)


def post_created(request, pk):
	profile = UserProfile.objects.get(pk = pk)
	test_message = "Thank you for following ArticleBuzz"
	if request.method == "POST":
		poster_email = "ArticleBuzz@gmail.com"
		followers = profile.followers.all
		follower_email_list = [follower.email for follower in followers if profile.follower.notifications == False] 
		send_mail ("new post", test_message, poster_email, follower_email_list)






