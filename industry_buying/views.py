import csv
import json
import pandas as pd
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.core import serializers
from .tasks import populate_db_with_csv_data
from industry_buying.models import IndustryDataCollection
from django.db.models import Count
from itertools import chain

# Create your views here.
class HomeView(TemplateView):
    template_name = "dashboard.html"
    def post(self, request):
        df=pd.read_csv('cunique.csv',sep=',')
        row_iter = df.iterrows()
        objs = []
        for index, row in row_iter:
            objs.append(IndustryDataCollection(
                Message = row["Message"],
                phone = row["phone"],
                truth = row["truth"],
                cube = row["cube"],
                google = row["google"],
                google_spam = row["google_spam"],
                google_not_spam = row["google_not_spam"],
                ibm = row["ibm"],
                ibm_spam = row["ibm_spam"],
                ibm_not_spam = row["ibm_not_spam"]
            ))
        IndustryDataCollection.objects.bulk_create(objs)

        # We can use celery as well for this task, so that user does not have to wait for the response if csv is too large.
        # CSV will be imported in the background
        # populate_db_with_csv_data.delay()
        return redirect('home')

def filter_industry_data(request):
    if request.method == "GET":
        query = request.GET.get("query")
        filtered_queryset = IndustryDataCollection.objects.filter(Message__icontains=query)
        filtered_queryset_count = filtered_queryset.count()
        ibm_count = filtered_queryset.values("ibm").annotate(the_count=Count('ibm'))
        cube_count = filtered_queryset.values("cube").annotate(the_count=Count('cube'))
        truth_count = filtered_queryset.values("truth").annotate(the_count=Count('truth'))
        google_count = filtered_queryset.values("google").annotate(the_count=Count('google'))
        all_querysets = list(chain(ibm_count, cube_count, truth_count, google_count))
        result = {
                    "total_matches":filtered_queryset_count
                }
        for c in all_querysets:
            for key, value in c.items():
                if key != "the_count":
                    if key in result:
                        if value not in result[key]:
                            result[key][value] = c["the_count"]
                    else:
                        result[key] = {value:c["the_count"]}
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        return HttpResponseBadRequest(content='Invalid method. Only GET method allowed')
        