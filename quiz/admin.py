from django.contrib import admin
from .models import Quiz, Question, Answer

# Настройка, чтобы ответы можно было добавлять прямо внутри вопроса
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # Сразу показывать 4 пустых поля для ответов

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['text', 'quiz']
    list_filter = ['quiz']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title']

# Если вам нужно управлять ответами отдельно, раскомментируйте строку ниже:
# admin.site.register(Answer)


# Текст в самой панели (в левом верхнем углу)
admin.site.site_header = "Панель управления Моего Проекта"

# Текст на главной странице админки
admin.site.index_title = "Добро пожаловать в админ-зону"

# Тег <title> вкладки браузера
admin.site.site_title = "Админка Моего Сайта"
