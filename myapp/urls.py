from django.contrib import admin
from django.urls import path
from myapp import views
from django.views.generic import TemplateView


urlpatterns = [
    
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('Scrape/', views.Scrape, name='Scrape'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('dataform/', views.dataform, name="Dataform"),
    path('dataform2/', views.dataform2, name="Dataform2"),
    path('dataform3/', views.dataform3, name="Dataform3"),
    path('sentiment_csv/', views.sentiment_csv, name="sentiment_csv"),
    path('sentimentform/', views.sentimentform, name="sentimentform"),
    path('cleaningform/', views.cleaningform, name="cleaningform"),
    path('courses/',views.courses,name="courses"),
    path('cleaning_csv/', views.cleaning_csv, name='cleaning_csv'),
    path('products/',views.products, name="products"),
    path('ebooks/',views.ebooks, name="ebooks"),
    path('books/',views.books, name="books"),
    path('course/',views.course, name="course"),
    path('table/', views.table, name="table"),
    path('amazon/', views.amazon, name="amazon"),
    path('sentiment/', views.sentiment, name="sentiment"),
]
