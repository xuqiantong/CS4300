from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json
from numpy import array, dot
from numpy.linalg import norm
import numpy as np
import sys
sys.path.append('../../scripts')
import scripts.database_connection as db
from .forms import SearchForm

@csrf_exempt
def home(request):
    db.select_test()
    return render_to_response('home.html')

@csrf_exempt
def similar_search(request):
    return render_to_response('search_similar.html')

@csrf_exempt
def custom_search(request):
    return render_to_response('search_custom.html')


def cosine_sim(a, b):


    dot = np.dot(a, b)
    norma = np.linalg.norm(a)
    normb = np.linalg.norm(b)
    if norma == 0:
        norma = 1
    if normb == 0:
        normb = 1
    cos = dot / (norma * normb)
    return cos


@csrf_exempt
def results(request):
    # MAX_THC = 34.0
    # MIN_THC = 1.0
    # MEAN_THC = 19.092282784673504
    RATING_WEIGHT = 1/4

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
    keys_vector = []
    with open('./data/keys_vector.json') as f:
        keys_vector = json.load(f)

    l = (dict(request.POST)).keys()
    k = {}
    for i in l:
        k = i
    q = json.loads(k)

    medical_lst = q.get("medicalEffects")
    if medical_lst == None:
        medical_lst = []
    desired_lst = q.get("desiredEffects")

    if desired_lst == None:
        desired_lst = []
    undesired_lst = q.get("undesiredEffects")
    if undesired_lst == None:
        desired_lst = []
    flavors_lst = q.get("flavors")
    if flavors_lst == None:
        flavors_lst = []
    aromas_lst = q.get("aromas")
    if aromas_lst == None:
        aromas_lst = []
    keyword_lst = q.get("keyword")
    if keyword_lst == None:
        keyword_lst = []

    state = q.get('state')
    city = q.get('city')
    strength = q.get('strength')

    data = db.select_test()

    output = []
    for datum in data:
        new_obj = {'strain_name': datum[0]}
        output.append(new_obj)

    print(output)

    return HttpResponse(json.dumps(output))

#
#     strain = {
#         'positive': desired_lst,
#         'negative_effects': undesired_lst,
#         'medical': medical_lst,
#         'aroma': aromas_lst,
#         'flavor_descriptors': flavors_lst,
#         'keywords': keyword_lst
#     }
#     search_strain_vector = strain_to_vector(strain, keys_vector)
#     #finding the relevant dimensions to run cosine sim on
#     relv_search = []
#     search_strain = []
#     for index in range(len(search_strain_vector)):
#         is_val = search_strain_vector[index]
#         if is_val == 1:
#             search_strain.append(1)
#             relv_search.append((index, search_strain_vector[index]))
#
#     scoring = []
#     for i in range(len(data)):
#         curr_strain = data[i]
#         curr_array = []
#         for relv_item in relv_search:
#             relv_index = relv_item[0]
#             curr_value = (curr_strain['vector'])[relv_index]
#             curr_array.append(curr_value)
#         cos_sim = cosine_sim(array(search_strain), array(curr_array))
#         rating = float(curr_strain['rating'])/5
#         score = RATING_WEIGHT * (cos_sim*rating) + (1-RATING_WEIGHT) * cos_sim
#         scoring.append((score, curr_strain))
#
#     sorted_strains = sorted(scoring, key=lambda tup: tup[0], reverse=True)
#     top_ten = sorted_strains[:9]
#     # for strain in top_ten:
#     #     print(strain[1]['positive'])
#     # replace data with the list of strain jsons we want to display on the front end
#     data = top_ten
#     return HttpResponse(json.dumps(data))
#
#
# def strain_to_vector(input, keys_vector):
#     vector_list_1 = input['positive'] + input['negative_effects'] + \
#         input['medical'] + input['aroma'] + input['flavor_descriptors']
#     vector_list = [x.lower() for x in vector_list_1]
#     cond_vector = []
#     #for now input 0s for the 40 keywords. add later after input keyword bar
#     #is implemented
#     for i in range(40):
#         cond_vector.append(0)
#     for key in keys_vector:
#         if key in vector_list:
#             cond_vector.append(1)
#         else:
#             cond_vector.append(0)
#
#     #rating
#     cond_vector.append(1)
#
#
#
#     return array(cond_vector)
