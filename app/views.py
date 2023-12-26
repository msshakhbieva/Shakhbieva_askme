from django.shortcuts import render
from django.forms import model_to_dict
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout

from app import models

from .forms import LoginForm, RegistrationForm, AskForm, AnswerForm, EditForm

top_users = models.Profile.objects.get_top_users()[:10]
top_tags = models.Tag.objects.get_hot_tags()[:10]


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
    context = create_content(models.Question.objects.get_recent_questions(), request)
    return render(request, 'index.html', context)


def hot(request):
    context = create_content(models.Question.objects.get_hot_questions(), request)
    return render(request, 'hot.html', context)


@login_required(login_url='login', redirect_field_name="continue")
def ask(request):
    ask_form = {}
    if request.method == 'POST':
        ask_form = AskForm(request.POST)
        if ask_form.is_valid():
            quest = models.Question.objects.create(
                title=ask_form.cleaned_data['title'],
                text=ask_form.cleaned_data['text'],
                author=models.Profile.objects.get(user=request.user)
            )
            quest.save()
            for tag_ in ask_form.cleaned_data['tags'].split(' '):
                to_add = models.Tag.objects.get_or_create(title=tag_)
                quest.tags.add(to_add[0].id)
            quest.save()
            if quest:
                return redirect("question", q_id=quest.id)

    elif request.method == 'GET':
        ask_form = AskForm()

    context = create_content_right()
    context['form'] = ask_form
    return render(request, 'question_form.html', context)


def question_page(request, q_id):
    form = {}
    if request.method == 'GET':
        form = AnswerForm()
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(reverse('login_page'))
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = models.Answer.objects.create(text=form.cleaned_data['text'],
                                                  question=models.Question.objects.get(id=q_id),
                                                  author=models.Profile.objects.get(user_id=request.user.id))
            answer.save()
            if answer:
                return redirect(reverse("question", args=[q_id]))

    try:
        question = models.Question.objects.get(id=q_id)
    except Exception:
        return render(request, 'not_found.html', create_content_right())

    context = create_content(models.Answer.objects.get_answers_for_question(q_id), request)
    context["question"] = question
    context['form'] = form

    return render(request, 'question_page.html', context)


def registration(request):
    user_form = {}
    if request.method == 'POST':
        user_form = RegistrationForm(data=request.POST, files=request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return redirect(reverse('register'))
    elif request.method == 'GET':
        user_form = RegistrationForm()

    context = create_content_right()
    context["form"] = user_form
    return render(request, 'registration.html', context)


def login_view(request):
    user_form = {}
    if request.method == 'POST':
        user_form = LoginForm(data=request.POST)
        if user_form.is_valid():
            user = authenticate(request, **user_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="Wrong Login/Password")
    elif request.method == 'GET':
        user_form = LoginForm()

    context = create_content_right()
    context["form"] = user_form
    return render(request, 'login.html', context)


@login_required(login_url='login', redirect_field_name="continue")
def profilesettings(request):
    form = {}
    if request.method == 'GET':
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.profile_related.avatar
        initial_data['bio'] = request.user.profile_related.bio
        form = EditForm(initial=initial_data)
    elif request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse("profile"))

    context = create_content_right()
    context['form'] = form
    return render(request, 'profilesettings.html', context)


def tag(request, tag_label):
    context = create_content(models.Question.objects.get_questions_for_tag(tag_label), request)
    try:
        context["tag_label"] = models.Tag.objects.get_tag_by_title(tag_label)
    except Exception:
        return render(request, 'not_found.html', create_content_right())
    context = create_content(models.Question.objects.get_questions_for_tag(tag_label), request)
    return render(request, 'tag.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@require_POST
@login_required(login_url='login_page', redirect_field_name="continue")
def like_question(request):
    quest_id = request.POST['question_id']
    quest = models.Question.objects.get(id=quest_id)
    try:
        like = models.LikeQ.objects.get(question_id=quest_id, user_id=request.user.profile_related.id)
    except models.LikeQ.DoesNotExist:
        like = models.LikeQ.objects.create(question=quest, user=request.user.profile_related)
        like.save()
    else:
        like.delete()

    quest.save()
    return JsonResponse(
        {'status': 'ok',
         'likes_count': quest.get_like_count()})


@require_POST
@login_required(login_url='login_page', redirect_field_name="continue")
def like_answer(request):
    answer_id = request.POST['answer_id']
    answer = models.Answer.objects.get(id=answer_id)
    try:
        like = models.LikeA.objects.get(answer_id=answer_id, user_id=request.user.profile_related.id)
    except models.LikeA.DoesNotExist:
        like = models.LikeA.objects.create(answer=answer, user=request.user.profile_related)
        like.save()
    else:
        like.delete()
    answer.save()
    return JsonResponse(
        {'status': 'ok',
         'likes_count': answer.get_like_count()})


@require_POST
@login_required(login_url='login_page', redirect_field_name="continue")
def correct(request):
    answer_id = request.POST['answer_id']
    answer = models.Answer.objects.get(id=answer_id)
    if answer.question.get_author_id() != request.user.id:
        JsonResponse(
            {'status': 'forbidden'})
        return
    answer.solution = not answer.is_solution()
    answer.save()
    return JsonResponse(
        {'status': 'ok',
         'solution': f'{answer.is_solution()}'}
    )
