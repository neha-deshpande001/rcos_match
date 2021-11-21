from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic

import json
import numpy as np

import eb_core.models
import eb_core.views
from .models import *


class Match_View(generic.UpdateView, eb_core.views.Match_View):
    permission_required = 'eb_core.main'
    model = eb_core.models.Individual_Sighting
    fields = ['completed', ]
    template_name = 'rcos_match/matching/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        match = context['results'].loc[self.kwargs['match_index']]

        bbox_set = self.object.sighting_bounding_box_set.all()

        images = [{'id': bbox.photo.image.name,
                'url': bbox.photo.compressed_image.url,
                'full_res': bbox.photo.image.url} for bbox in bbox_set]

        boxes = {bbox.photo.image.name: [{
            'bbox': [bbox.x, bbox.y, bbox.w, bbox.h],
            'category_id': self.object.pk
        }] for bbox in bbox_set}

        given_code = self.object.seek_identity
        str_given_code = str(given_code)

        bbox_set = match.individual.individual_sighting_set.last().sighting_bounding_box_set.all()

        matchImages = [{'id': bbox.photo.image.name,
                'url': bbox.photo.compressed_image.url,
                'full_res': bbox.photo.image.url} for bbox in bbox_set]

        matchBoxes = {bbox.photo.image.name: [{
            'bbox': [bbox.x, bbox.y, bbox.w, bbox.h],
            'category_id': 1
        }] for bbox in bbox_set}

        known_thumbnails = {
            '':
            {i: eb_core.models.Sighting_Photo.objects.get(image=image['id']).thumbnail.url
            for i, image in enumerate(matchImages)}
        }
        unknown_thumbnails = {
            '':
            {i: eb_core.models.Sighting_Photo.objects.get(image=image['id']).thumbnail.url
            for i, image in enumerate(images)}
        }


        context |= {
            'match': match,
            'images': json.dumps(images),
            'matchImages': json.dumps(matchImages),
            'given_code': str_given_code,
            'match_index': self.kwargs['match_index'],
            'individual_id': match.individual.id,
            'boxes': json.dumps(boxes),
            'matchBoxes': json.dumps(matchBoxes),
            'known_thumbnails': known_thumbnails,
            'unknown_thumbnails': unknown_thumbnails,
        }

        return context

    def get_success_url(self):
        return reverse('individual view', kwargs={'pk': self.object.individual.pk})

    def form_valid(self, form):
        match = super().get_context_data(self.kwargs)['results'].loc[self.kwargs['match_index']]
        self.object.individual = match.individual
        self.object.save()

        return super().form_valid(form)


class Table_View(eb_core.views.Match_View):
    permission_required = 'eb_core.main'
    model = eb_core.models.Individual_Sighting
    template_name = 'rcos_match/table/seek_table.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        given_code = self.object.seek_identity

        table_data = []
        for i, row in context['results'].iterrows():
            temp = [row.individual.name, row.individual.pk, "{0:0.4f}".format(row.seek_score), " ".join(str(row.seek_identity))]
            table_data.append(temp)

        context |= {
            'table_data': table_data,
            'given_code':" ".join(str(given_code))
        }

        return context
