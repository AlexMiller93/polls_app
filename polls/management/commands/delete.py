from django.core.management.base import BaseCommand

from polls.models import Category, Question

class Command(BaseCommand):
    help = 'Clean data about questions from database'
    
    def handle(self, *args, **options):
        categories = Category.objects.all()
        questions = Question.objects.all()
        
        if categories and questions:
            categories.delete()
            questions.delete()
        
            self.stdout.write(self.style.SUCCESS('Данные успешно удалены'))
            
        else:
            self.stdout.write(self.style.ERROR('Данные не записаны'))