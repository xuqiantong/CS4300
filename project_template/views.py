from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader

# Create your views here.
def search(request):
    query = request.GET.get('search')
    if not query:
        output_message = ''
        data = []
    else:
        output_message = query
        query_result_list = range(15)
        paginator = Paginator(query_result_list, 10)
        page = request.GET.get('page')
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

    return render_to_response(
        'search.html',
        {
            'output_message': output_message,
            'data': data,
            'magic_url': request.get_full_path(),
        }
    )