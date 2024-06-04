from django.core.management.base import BaseCommand
import requests

from core.settings import URL
from polls.models import Category, Question

class Command(BaseCommand):
    help = 'Parse and save questions from outer url'

    '''
    URL='https://opentdb.com/api.php'
    
    +'?amount=10&type=boolean'
    +'?amount=10&type=multiple'
    
    + ?difficulty=easy&type=boolean
    '''
    
    def _get_url_for_type(url: str, type: str) -> str: 
        """ """
        pass
    
    
    def handle(self, *args, **options):
        # todo: разделить логику на булевые и многоответные вопросы, 
        # в последних добавить сохранение всех ответов
        
        # get_url_for_type(URL, )
        url = URL + '?amount=10&type=multiple'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('response_code') != 0: # ok
                pass
                # try again
            
            
                # handle question type 
                # type = item.get('type')
                
                # if type == 'boolean':
                #     pass
                # else:
                #     pass
                
            results = data.get('results')
            for result in results:
                
                category = Category.objects.create(
                    name = result['category'],
                )
                question = Question.objects.create(
                    category=category,
                    question_type = result['type'],
                    difficulty = result['difficulty'],
                    text = result['question'],
                    correct_answer = result['correct_answer']
                )
                
                
                question.save()
                category.save()
        
            self.stdout.write(self.style.SUCCESS('Данные успешно загружены'))
        else:
            self.stdout.write(self.style.ERROR('Не удалось загрузить данные. Код ошибки: {}'.format(response.status_code)))