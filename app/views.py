from django.shortcuts import render
from django.core.paginator import Paginator

from app import models

top_users = models.Profile.objects.all()[:10]
top_tags = models.Tag.objects.all()[:10]


def create_content_right():
    content = {
        "tags": top_tags,
        "users": top_users,
    }

    return content


def create_content(objects, request):
    """Функция осуществляет пагинацию
    переданных объектов и
    добавляет контент для боковой панели"""
    page = pagination(objects, request)
    content = create_content_right()
    content["content"] = page
    return content


PER_PAGE = 10


def pagination(objects, request):
    paginator = Paginator(objects, PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page


def index(request):
    context = create_content(models.Question.objects.get_hot_questions(), request)
    return render(request, 'index.html', context)


def ask(request):
    context = create_content_right()
    return render(request, 'question_form.html', context)


def question_page(request, q_id):
    question = models.Question.objects.get(id=q_id)

    context = create_content(models.Answer.objects.get_answers_for_question(q_id), request)
    context["question"] = question

    return render(request, 'question_page.html', context)


def registration(request):
    context = create_content_right()
    return render(request, 'registration.html', context)


def login(request):
    context = create_content_right()
    return render(request, 'login.html', context)


def profilesettings(request):
    context = create_content_right()
    return render(request, 'profilesettings.html', context)


def tag(request, tag_label):
    context = create_content(models.Question.objects.get_questions_for_tag(tag_label), request)
    context["tag_label"] = models.Tag.objects.get_tag_by_title(tag_label)
    return render(request, 'tag.html', context)