from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import SearchForm

# Create your views here.
# def search(request):
#     query = request.GET.get('search')
#     if not query:
#         output_message = ''
#         data = []
#     else:
#         output_message = query
#         query_result_list = range(15)
#         paginator = Paginator(query_result_list, 10)
#         page = request.GET.get('page')
#         try:
#             data = paginator.page(page)
#         except PageNotAnInteger:
#             data = paginator.page(1)
#         except EmptyPage:
#             data = paginator.page(paginator.num_pages)

#     return render_to_response(
#         'search.html',
#         {
#             'output_message': output_message,
#             'data': data,
#             'magic_url': request.get_full_path(),
#             'form': SearchForm()
#         }
#     )

def home(request):
    return render_to_response('home.html')

def similar_search(request):
    return render_to_response('search_similar.html')

def custom_search(request):
    return render_to_response('search_custom.html')


'''
    MAX_THC = 34.0
    MIN_THC = 1.0
    MEDIAN_THC = 20.0
    MEAN_THC = 19.092282784673504

    print(request)
    print("asdlkfjalskdfjasfldkjasdflkj")
'''

@csrf_exempt
def results(request):
    MAX_THC = 34.0
    MIN_THC = 1.0
    MEAN_THC = 19.092282784673504

    q = QueryDict(request.body, mutable=True)

    '''
    strength = q['strength']
    # TODO: determine which effects go in which category,
    effects = q['all_effects']
    medical = effects['medical']
    positive = effects['positive']
    negative = effects['negative']
    flavor = effects['flavor']
    aroma = effects['aroma']

    #TODO: search database for strains with these medical, positive, negative, flavor, aroma
    strains = search()
    '''
    data = {}
    with open('./data/combined_cleaned_data.json', encoding="utf8") as f:
        data = json.loads(f.read())

    medical_lst = q.getlist("medicalEffects[]")
    desired_lst = q.getlist("desiredEffects[]")
    undesired_lst = q.getlist("undesiredEffects[]")
    flavors_lst = q.getlist("flavors[]")
    aromas_lst = q.getlist("aromas[]")
    
    state = request.POST.get('state')
    city = request.POST.get('city')
    strength = request.POST.get('strength')

    
    strains = []
    scoring = []
    for i in range(len(data)):
        curr_strain = data[i]
        curr_thc = 0
        if 'percentages' in curr_strain and 'THC' in curr_strain['percentages']:
            curr_thc = curr_strain['percentages']['THC']
        else:
            curr_thc = MEAN_THC
        actual_strength = strength / MAX_THC
        compare_score = curr_thc / MAX_THC 
        strength_score = MAX_THC / abs(compare_score - actual_strength)
        rating_score = curr_strain['rating']/5
        overall_score = strength_score * 30 + rating_score * 70
        scoring.append((overall_score, strain))


    sorted_strains = sorted(scoring, key=lambda tup: tup[0], reverse=True)
    output = [i[1] for i in sorted_strains]


    # replace data with the list of strain jsons we want to display on the front end
    data = [{"strain_name": "Cheese"}, {"strain_name": "Strawberry"}]
    return HttpResponse(json.dumps(data))
    # return HttpResponse(json.dumps(output))
