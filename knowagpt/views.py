from django.http import JsonResponse
import os
import transformers
from django.conf import settings
from django.shortcuts import HttpResponse
import urllib.parse
from rest_framework.decorators import api_view

@api_view(['GET'])
def qa_answer(request):

    if 'Authorization' not in request.headers:
        return JsonResponse({'error': 'Unauthorized: Token is missing'}, status=401)

    authorization = request.headers['Authorization']
    if not authorization.startswith('Bearer '):
        return JsonResponse({'error': 'Unauthorized: Token is missing'}, status=401)

    token = authorization[7:]
    if token != '12345678':
        return JsonResponse({'error': 'Unauthorized: Token is invalid'}, status=401)
    
    with open(os.path.join(settings.BASE_DIR, 'knowagpt', request.GET.get('topic') + '.txt'), 'r') as file:
        essay = file.read()
    context = essay
    q_a_model = transformers.pipeline('question-answering')
    question = request.GET.get('question')
    answers = q_a_model({
        'context': context,
        'question': question
    })

    return JsonResponse({'answer': answers['answer']}) # JSON response

@api_view(['GET'])
def create_file(request):
        request_content = request.GET.get('content')
        request_file_name = request.GET.get('file_name')
        query_string = "content="+ request_content +"&file_name=" + request_file_name
        parsed_query = urllib.parse.parse_qs(query_string)
        file_content = parsed_query.get("content")[0]
        file_name = parsed_query.get("file_name")[0]
        file_path = "knowagpt"

        if file_path is None or file_name is None:
            return HttpResponse("file_path and file_name cannot be None.")

        full_path = os.path.join(file_path, file_name)
        
        data = file_content

        with open(full_path, "w") as file:
            file.write(data)
        
        return HttpResponse("File created successfully.")
