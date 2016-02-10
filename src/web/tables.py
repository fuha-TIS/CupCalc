import django_tables2 as tables
from .models import Person

class PersonTable(tables.Table):
    class Meta:
        model = Person
        order_by = ("last_name", "first_name")
        attrs = { 'class':'paleblue' }

class PersonList(tables.SingleTableView):
    model = Person
    table_class = PersonTable

