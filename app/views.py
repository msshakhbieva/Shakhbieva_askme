from django.shortcuts import render
from django.http import HttpResponse


QUESTIONS = [
        {
            "title": f"Question #{i}",
            "text": f"Question text #{i}",
            "id": i,
            "tags": ["bebra", "adidas", "tag"],
            "answers": [
                {
                    "text": f"Answer text #{k}",
                } for k in range(3)
            ]
        } for i in range(20)
    ]


def index(request):
    context = {
        "questions": QUESTIONS
    }
    return render(request, 'index.html', context)


def ask(request):
    return render(request, 'question_form.html')


def question_page(request, q_id):
    question = QUESTIONS[q_id]
    context = {
        "question": question
    }
    return render(request, 'question_page.html', context)


def registration(request):
    return render(request, 'registration.html')


def login(request):
    return render(request, 'login.html')


def profilesettings(request):
    return render(request, 'profilesettings.html')


def tag(request, tag_label):
    questions = []
    for question in QUESTIONS:
        if tag_label in question["tags"]:
            questions.append(question)

    context = {
        "questions": questions,
        "tag_label": tag_label
    }
    return render(request, 'tag.html', context)