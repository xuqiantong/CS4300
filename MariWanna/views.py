from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json
# import scripts.database_connection as db
# from scipy import spatial
from numpy import array, dot
from numpy.linalg import norm
import numpy as np



from .forms import SearchForm

def home(request):
    return render_to_response('home.html')

def similar_search(request):
    return render_to_response('search_similar.html')

def custom_search(request):
    return render_to_response('search_custom.html')

def cosine_sim(a, b):
    RATING_WEIGHT = 3
    CONDITIONS_WEIGHT = 5

    w = np.zeros((187)) #40, 146, 1
    for i in range(41, 186):
        w[i] = CONDITIONS_WEIGHT
    w[186] = RATING_WEIGHT

    dot = np.dot(w*a, w*b)
    norma = np.linalg.norm(w*a)
    normb = np.linalg.norm(w*b)
    cos = dot / (norma * normb)
    return cos


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

    strain = {
        'positive': desired_lst,
        'negative_effects': undesired_lst,
        'medical': medical_lst,
        'aroma': aromas_lst,
        'flavor_descriptors': flavors_lst,
        'keywords': keyword_lst
    }
    search_strain_vector = strain_to_vector(strain, keys_vector)

    scoring = []
    for i in range(len(data)):
        curr_strain = data[i]
        cos_sim = cosine_sim(search_strain_vector, array(curr_strain['vector']))
        # result = 1 - spatial.distance.cosine(search_strain_vector, array(curr_strain['vector']))
        scoring.append((cos_sim, curr_strain))

    sorted_strains = sorted(scoring, key=lambda tup: tup[0], reverse=True)
    top_ten = sorted_strains[:9]
    # replace data with the list of strain jsons we want to display on the front end
    data = top_ten
    return HttpResponse(json.dumps(data))


def strain_to_vector(input, keys_vector):
    average_inputs = []
    with open('./data/averages.json') as f:
        average_inputs = json.load(f)

    vector_list_1 = input['positive'] + input['negative_effects'] + \
        input['medical'] + input['aroma'] + input['flavor_descriptors']

    vector_list = []
    for vector in vector_list_1:
        vector_two = vector.lower()
        vector_list.append(vector_two)

    cond_vector = []
    for key,cur_avg in zip(keys_vector, average_inputs):
        if key in vector_list:
            cond_vector.append(1)
        else:
            cond_vector.append(cur_avg)

    #rating
    cond_vector.append(1)

    # keyword_lst = input['keyword']
    for i in range(40):
        cond_vector.append(0)

    return array(cond_vector)



#     MAX_THC = 34.0
#     MIN_THC = 1.0
#     MEAN_THC = 19.092282784673504
#
