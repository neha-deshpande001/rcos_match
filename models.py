from django.db import models

import django_tables2 as tables

from eb_core.models import Seek_Identity
from .models import *

class SeekTable(tables.Table):
    class Meta:
        model = Seek_Identity

class SeekTableView(tables.SingleTableView):
    table_class = SeekTable
    queryset = Seek_Identity.objects.all()
    template_name = "seek_table.html"
