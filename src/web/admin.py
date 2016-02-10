from django.contrib import admin
from web.models import *
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
import pickle

ITEMS_PER_PAGE = 10000

def merge(modeladmin, request, queryset):
    #selected contains list of ID's of selected items
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    #ct = name of the model
    ct = ContentType.objects.get_for_model(queryset.model)
    request.session['data'] = pickle.dumps(selected)
    request.session['model'] = pickle.dumps(ct)
    return HttpResponseRedirect('/merge/')
merge.short_description = "Merge selected items"

class ClubAdmin(admin.ModelAdmin):
    actions = [merge]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = [merge]

class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','club', 'category','ccard')
    list_filter = ('club', 'category')
    list_per_page = ITEMS_PER_PAGE
    actions = [merge]

class ResultAdmin(admin.ModelAdmin):
    list_display = ('person', 'run', 'result_time', 'status', 'points', 'position_run')
    list_filter = ('run', 'status')
    list_per_page = ITEMS_PER_PAGE

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('xmlfile', 'season')
    list_filter = ('xmlfile', 'season')

class RunAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'season')
    list_per_page = ITEMS_PER_PAGE

class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')

class PositionAdmin(admin.ModelAdmin):
    list_display = ('position_season','position_category','season','person','points')
    list_per_page = ITEMS_PER_PAGE




admin.site.register(Season, SeasonAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Run, RunAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Document, DocumentAdmin)
