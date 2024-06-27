from django.urls import path

from avito import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),  # http://127.0.0.1:8000
    # path('about/', views.about, name='about'),
    path('otklik/', views.OtklikListView.as_view(), name='otklik'),
    path('post/<slug:post_slug>/', views.PostDetailView.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.PostCategoryListView.as_view(), name = 'category'),
    path('addpost/', views.PostCreateView.as_view(), name = 'addpost'),
    # path('addmessage/', views.MessageCreateView.as_view(), name = 'addmessagesite'),
    path('addmessage/<slug:post_slug>/', views.MessageCreateView.as_view(), name='addmessage'),
    path('edit/post/<slug:post_slug>/', views.PostUpdateView.as_view(), name = 'editpost'),
    path('delete/post/<slug:post_slug>/', views.PostDeleteView.as_view(), name ='deletepost'),
    path('otklik/accept/<int:pk>/', views.accept_otklik, name='accept_otklik'),
    path('otklik/delete/<int:pk>/', views.delete_otklik, name='delete_otklik'),
]