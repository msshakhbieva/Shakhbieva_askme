"""
URL configuration for askme_shakhbieva project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('ask/', views.ask, name='ask'),
    path('question/<int:q_id>/', views.question_page, name='question'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_view, name='login'),
    path('profile/edit/', views.profilesettings, name='profile'),
    path('tag/<str:tag_label>', views.tag, name='tag'),
    path('hot/', views.hot, name='hot'),
    path('logout', views.logout_view, name="logout"),
    path('like/question', views.like_question, name='like_q'),
    path('like/answer', views.like_answer, name='like_a'),
    path('answer/correct', views.correct, name='correct'),

    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
