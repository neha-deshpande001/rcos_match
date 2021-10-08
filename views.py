from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

import json
import numpy as np

from eb_core.models import Individual_Sighting, Seek_Identity, Individual
from eb_core.views import individual_sighting_list
from .forms import *
from .models import *


def get_individual_seek():
    return [
        individual.individual_sighting_set.latest('id').seek_identity for individual in Individual.objects.all()
        if individual.individual_sighting_set.count()
    ]


def matching(request, individual_id, match_index):

    individual_sighting = get_object_or_404(
        Individual_Sighting, pk=individual_id)

    bbox_set = individual_sighting.sighting_bounding_box_set.all()

    images = [{'id': bbox.photo.image.name,
               'url': bbox.photo.compressed_image.url,
               'full_res': bbox.photo.image.url} for bbox in bbox_set]

    boxes = {bbox.photo.image.name: [{
        'bbox': [bbox.x, bbox.y, bbox.w, bbox.h],
        'category_id': 1
    }] for bbox in bbox_set}

    given_code = Seek_Identity_Form(request.GET).save(commit=False)
    str_given_code = str(given_code)

    seek_identities = np.array(get_individual_seek(), dtype=object)
    codes = np.array([np.array(code) for code in seek_identities])

    if 'binary' in request.GET and request.GET['binary'] == 'on':
        total_match = np.all((codes == given_code) | (
            codes == '?') | (np.array(given_code) == '?'), axis=1)
        seek_identities = seek_identities[total_match]
        codes = codes[total_match]

    if 'individual' in request.GET:
        total_match = np.array([seek_identity.individual_sighting.individual is not None and
                                seek_identity.individual_sighting.individual.pk ==
                                int(request.GET['individual'])
                                for seek_identity in seek_identities])
        seek_identities = seek_identities[total_match]
        codes = codes[total_match]

    scores = np.mean(codes == given_code, axis=1) - \
        0.4*np.mean(codes == '?', axis=1)

    results = np.column_stack((scores, seek_identities))[np.argsort(-scores)]

    results_list = list()
    for score, seek in results:
        temp_dict = {'seek_code': str(seek), 'score': score}
        if seek.individual_sighting.individual:
            temp_dict['name'] = seek.individual_sighting.individual.name
        else:
            temp_dict['name'] = "Unknown"
        temp_dict['id'] = seek.individual_sighting.id
        results_list.append(temp_dict)


    individual_id_match = results_list[match_index]['id']
    individual_sighting = get_object_or_404(
        Individual_Sighting, pk=individual_id_match)

    bbox_set = individual_sighting.sighting_bounding_box_set.all()

    matchImages = [{'id': bbox.photo.image.name,
               'url': bbox.photo.compressed_image.url,
               'full_res': bbox.photo.image.url} for bbox in bbox_set]

    matchBoxes = {bbox.photo.image.name: [{
        'bbox': [bbox.x, bbox.y, bbox.w, bbox.h],
        'category_id': 1
    }] for bbox in bbox_set}

    context = {
        'results_list': json.dumps(results_list), # to use in javascript
        'results': results, # to use in html
        'images': json.dumps(images),
        'matchImages': json.dumps(matchImages),
        'given_code': str_given_code,
        'match_index': match_index,
        'form': Further_Review_Form(),
        'individual_id': individual_id,
        'boxes': json.dumps(boxes),
        'matchBoxes': json.dumps(matchBoxes),
    }

    return render(request, 'rcos_match/matching/index.html', context)


def matching_submit(request, individual_id, match_index):
    if request.method == 'POST':
        form = Match_Form(request.POST)
        # print("form.data:",form)
        indiv = form.data['indiv']
        indiv_sight = form.data['indiv_sight']

        indiv_sight.individual = indiv
        indiv_sight.save()
        
    return redirect(individual_sighting_list)

# def matching_submit(request, individual_id, match_index):
#     individual_sighting = get_object_or_404(
#         Individual_Sighting, pk=individual_id)

#     bbox_set = individual_sighting.sighting_bounding_box_set.all()

#     images = [{'id': bbox.photo.image.name,
#                'url': bbox.photo.compressed_image.url,
#                'full_res': bbox.photo.image.url} for bbox in bbox_set]


#     given_code = Seek_Identity_Form(request.GET).save(commit=False)
#     str_given_code = str(given_code)
#     seek_identities = np.array(get_individual_seek(), dtype=object)
#     codes = np.array([np.array(code) for code in seek_identities])

#     if 'binary' in request.GET and request.GET['binary'] == 'on':
#         total_match = np.all((codes == given_code) | (
#             codes == '?') | (np.array(given_code) == '?'), axis=1)
#         seek_identities = seek_identities[total_match]
#         codes = codes[total_match]

#     if 'individual' in request.GET:
#         total_match = np.array([seek_identity.individual_sighting.individual is not None and
#                                 seek_identity.individual_sighting.individual.pk ==
#                                 int(request.GET['individual'])
#                                 for seek_identity in seek_identities])
#         seek_identities = seek_identities[total_match]
#         codes = codes[total_match]

#     scores = np.mean(codes == given_code, axis=1) - \
#         0.4*np.mean(codes == '?', axis=1)

#     results = np.column_stack((scores, seek_identities))[np.argsort(-scores)]

#     results_list = list()
#     for score, seek in results:
#         temp_dict = {'seek_code': str(seek), 'score': score}
#         if seek.individual_sighting.individual:
#             temp_dict['name'] = seek.individual_sighting.individual.name
#         else:
#             temp_dict['name'] = "Unknown"
#         temp_dict['id'] = seek.individual_sighting.id
#         results_list.append(temp_dict)



#     individual_id_match = results_list[match_index]['id']
#     individual_sighting_match = get_object_or_404(
#         Individual_Sighting, pk=individual_id_match)

#     if request.method == 'POST':
#         # Unknown Individual
#         form = Unknown_Individual_Form(request.POST, instance=individual_sighting)
#         if form.is_valid():
#             form.save()

#         # Selected Match Individual
#         form = Selected_Match_Individual_Form(request.POST, instance=individual_sighting_match)
#         if form.is_valid():
#             form.save()

#         # Needs Further Review
#         form = Further_Review_Form()
#         if form.is_valid():
#             form.save()

#     return redirect(individual_sighting_list)


def table(request):
    context = {
        'tabledata': get_individual_seek()
    }
    return render(request, "rcos_match/table/seek_table.html", context)
