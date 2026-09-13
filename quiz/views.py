import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Answer

def index(request):
    """Главная страница. Доступна всем, но кнопки 'Начать' управляются через JS"""
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/index.html', {'quizzes': quizzes})

def ajax_login(request):
    """Обработка входа через AJAX"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Вы успешно вошли!'})
        return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    
    # Если GET-запрос, отдаем чистую HTML-форму для модального окна
    form = AuthenticationForm()
    html = render_to_string('quiz/partials/login_form.html', {'form': form}, request=request)
    return JsonResponse({'html': html})

def ajax_register(request):
    """Обработка регистрации через AJAX"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Регистрация успешна!'})
        return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    
    form = UserCreationForm()
    html = render_to_string('quiz/partials/register_form.html', {'form': form}, request=request)
    return JsonResponse({'html': html})

def get_quiz_card(request, quiz_id):
    """Возвращает динамический HTML-контейнер викторины (только для авторизованных)"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'authenticated': False, 
            'message': 'Для прохождения теста необходимо авторизоваться.'
        })
        
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.questions.values_list('id', flat=True))
    
    if not questions:
        return JsonResponse({'authenticated': True, 'html': '<div class="uk-alert-danger" uk-alert>В тесте нет вопросов.</div>'})
        
    # Инициализация сессии
    request.session['quiz_questions'] = questions
    request.session['current_index'] = 0
    request.session['score'] = 0
    
    # Рендерим стартовый каркас игрового поля
    html = render_to_string('quiz/partials/quiz_game_layout.html', {'quiz': quiz}, request=request)
    return JsonResponse({'authenticated': True, 'html': html})

@login_required(login_url='/')  # Для AJAX вернет редирект или обработается на клиенте
def ajax_next_question(request):
    """Выдача следующего вопроса и обработка ответа через AJAX"""
    questions = request.session.get('quiz_questions', [])
    current_index = request.session.get('current_index', 0)
    
    if request.method == 'POST':
        selected_id = request.POST.get('answer_id')
        if selected_id:
            answer = Answer.objects.filter(id=selected_id, is_correct=True).exists()
            if answer:
                request.session['score'] += 1
        
        current_index += 1
        request.session['current_index'] = current_index

    # Проверка завершения
    if current_index >= len(questions):
        score = request.session.get('score', 0)
        total = len(questions)
        html = render_to_string('quiz/partials/result_card.html', {'score': score, 'total': total}, request=request)
        return JsonResponse({'finished': True, 'html': html})

    # Берем вопрос
    question_id = questions[current_index]
    question = Question.objects.get(id=question_id)
    progress = int((current_index / len(questions)) * 100)
    
    html = render_to_string('quiz/partials/question_card.html', {
        'question': question,
        'progress': progress,
        'current_num': current_index + 1,
        'total_num': len(questions)
    }, request=request)
    
    return JsonResponse({'finished': False, 'html': html})
