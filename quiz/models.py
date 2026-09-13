from django.db import models

class Quiz(models.Model):
    """Сама викторина (тема)"""
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.title

class Question(models.Model):
    """Вопрос, привязанный к конкретной викторине"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name="Текст вопроса")

    def __str__(self):
        return self.text

class Answer(models.Model):
    """Вариант ответа (их может быть несколько для одного вопроса)"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255, verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Это правильный ответ?")

    def __str__(self):
        return self.text
