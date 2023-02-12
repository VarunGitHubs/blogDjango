from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#from . import views
from .views import HomeView, ArticleDetailView, ArticlePostView,UpdatePostView, LikePostView, AddCategoryView, CategoryView,AddCommentView, CategoryListView, ProfileView, UserProfileUpdateView, AddFollower, RemoveFollower

urlpatterns = [
    #path('', views.home, name = 'home'),
    path('', HomeView.as_view(), name = 'home'),
    path("article/<int:pk>", ArticleDetailView.as_view(), name = 'article-detail'),
    path("add_article/", ArticlePostView.as_view(), name = "add-article"),
    path('update_article/<int:pk>', UpdatePostView.as_view(), name = 'update-article'),
    path('like/<int:pk>', LikePostView, name = 'like_post'),
    path('add_category/', AddCategoryView.as_view(), name = 'add-category'),
    path('category/<str:cats>', CategoryView, name = 'category'),
    path('article/<int:pk>/comment', AddCommentView.as_view(), name = 'add-comment'),
    path('category-list/', CategoryListView, name = 'category-list'),
    path('profile/<int:pk>', ProfileView.as_view(), name = 'profile'),
    path('profile/edit/<int:pk>', UserProfileUpdateView.as_view(), name = 'edit-profile'),
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name = 'add-follower'),
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name = 'remove-follower')
]


#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)