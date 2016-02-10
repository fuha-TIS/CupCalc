# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotModified
from django.core.urlresolvers import reverse
from .forms import UploadRun, EvalForm01, EvalForm02, EvalForm03, EvalForm04, CreateSeason, ClubForm, PersonForm, CategoryForm
from parser import Parser
from web.models import Document, Category, Season, Club, Person, Result, Position, Run
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from eval1 import Evaluation1
from eval2 import Evaluation2
from eval3 import Evaluation3
from eval4 import Evaluation4
import unicodedata
import pickle
from itertools import chain
from djqscsv import render_to_csv_response

def index(request):
    season = Season.objects.all()
    if request.method == 'POST':
        form = CreateSeason(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('web:index'))
    else:
        form = CreateSeason()

    return render(request, 'web/index.html', { 'form':form, 'season':season })

def runs(request):
    if request.method == 'POST':
        form = UploadRun(request.POST, request.FILES)
        if form.is_valid():
            xmlFile = Document(xmlfile = request.FILES['xml_file'], season = Season.objects.get(pk=int(request.POST['season'])))
            xmlFile.save()
            return HttpResponseRedirect(reverse('web:parse', kwargs={'documentPk':xmlFile.pk}))
    else:
        form = UploadRun()
    documents = Document.objects.all()
    return render(request,'web/runs.html', {'form': form, 'documents': documents})

def parse(request, documentPk):
    document = Document.objects.get(pk=documentPk)
    categories = Category.objects.all()
    runs = Run.objects.all()
    persons = Person.objects.all()
    results = Result.objects.all()
    xmlParser = Parser('/home/django/django_project' + document.xmlfile.url).select_parser()
    newRun = Run(name=xmlParser.event_data.get('name','NEPOMENOVANY BEH').strip(), date=xmlParser.event_data.get('date','1700-01-01' ), season=document.season)
    runAlreadyInDatabase = False
    for everyRun in runs:
        if everyRun.season == newRun.season and everyRun.name == newRun.name and str(everyRun.date) == newRun.date:
            runAlreadyInDatabase = True
            runInXML = everyRun
            break
    if  runAlreadyInDatabase == False:
        runInXML = newRun
        newRun.save()
    for key in xmlParser.runners_data.keys():
        categoryAlreadyInDatabase = False
        tmpCat = Category(name=key.strip())
        for runnerCategory in categories:
            if tmpCat.name == runnerCategory.name:
                categoryAlreadyInDatabase = True
                break
        if categoryAlreadyInDatabase == False:
            tmpCat.save()

        for xmlPerson in xmlParser.runners_data[key]:
            try:
                newClub = Club.objects.get(name=unicode(xmlPerson.get('club','N/A')).strip())
            except Club.DoesNotExist:
                newClub = Club(name=unicode(xmlPerson.get('club','N/A')).strip())
                newClub.save()
            newPerson = Person(first_name = xmlPerson['meno'].strip(), last_name = xmlPerson['priezvisko'].strip(), category = Category.objects.get(name=key.strip()), club= Club.objects.get(name=unicode(xmlPerson.get('club','N/A')).strip()))
            newPerson.ccard=xmlPerson.get('ccard',0)
            newPerson.person_id=xmlPerson.get('person_id',"0")
            if len(newPerson.person_id) >= 3:
                for club in Club.objects.all():
                    pass
            if newPerson.ccard is None:
                newPerson.ccard = 0
            personAlreadyInDatabase = False
            for everyPerson in persons:
                if newPerson.first_name == everyPerson.first_name and newPerson.last_name == everyPerson.last_name and newPerson.category == everyPerson.category:
                    personAlreadyInDatabase = True
                    personInXML = everyPerson
                    break
            if personAlreadyInDatabase == False:
                personInXML = newPerson
                newPerson.save()
            newRes = Result(person=Person.objects.get(pk=personInXML.pk), run=Run.objects.get(pk=runInXML.pk),start_time=xmlPerson.get('starttime','00:00:00'),finish_time=xmlPerson.get('finishtime','00:00:00'), status=xmlPerson['status'], points=Decimal("0"), position_run=xmlPerson.get('position',0))
            result_time=xmlPerson.get('time','00:00:00')
            if result_time.count(":") == 1:
                result_time = "00:" + result_time
            if result_time.count(":") > 0:
                time = result_time.encode('ascii', 'ignore')
                result_time = timeSum(time)
            newRes.result_time = result_time
            resultAlreadyInDatabase = False
            for everyResult in results:
                if personInXML == everyResult.person and runInXML == everyResult.run:
                    resultAlreadyInDatabase = True
                    break
            if resultAlreadyInDatabase == False:
                newRes.save()

    return HttpResponseRedirect(reverse('web:databasePerson'))

def timeSum(timeString):
    array = timeString.split(':')
    time = ( int(array[0])*3600 + int(array[1])*60 + int(array[2]) )
    return time

def eval1(request):
    if request.method == 'POST':
        form = EvalForm01(request.POST)
        if form.is_valid():
            runs = form.cleaned_data['runs']
            value = form.cleaned_data['value']
            value2 = form.cleaned_data['value2']
            first = form.cleaned_data['first']
            last = form.cleaned_data['last']
            percents = form.cleaned_data['percents']
            if runs is not None:
                runs_for_calculation = Run.objects.filter(season=runs)
                for run_name in runs_for_calculation:
                    inputList = []
                    personList = Person.objects.filter(runs = Run.objects.get(pk = run_name.pk))
                    for persona in personList:
                        if Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk = run_name.pk)).status != 'OK':
                            continue
#                        time = str(unicodedata.normalize('NFKD', Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk = run_name.pk)).result_time).encode('ascii', 'ignore'))
                        time = Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk = run_name.pk)).result_time
                        seconds = int(time)
                        points = Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk = run_name.pk)).points
                        inputList.append([persona.pk, seconds, points])
                    if value is not None:
                        result = Evaluation1(inputList, 1, int(value)).outputList
                        vyhodnot(result, run_name.pk )
                    elif value2 is not None:
                        result = Evaluation1(inputList, 2, int(value2)).outputList
                        vyhodnot(result, run_name.pk )
                    elif first is not None and last is not None and percents is not None:
                        result = Evaluation1(inputList, 3, int(first), int(last), int(percents)).outputList
                        vyhodnot(result, run_name.pk )
                return HttpResponseRedirect(reverse('web:databasePerson'))
    else:
        form = EvalForm01()
    return render(request, 'web/eval1.html', {'form':form})

def vyhodnot(scoredResults, scoredRunId):
    scoredRun = Run.objects.get(pk=int(scoredRunId))
    for scoredResult in scoredResults:
        scoredPerson = Person.objects.get(pk=scoredResult[0])
        databaseResult = Result.objects.get(run = scoredRun, person = scoredPerson)
        databaseResult.points = Decimal.from_float(scoredResult[2])
        databaseResult.save()
        databaseResult = None
    results = Result.objects.all()
    nullPoints()
    for i in range(len(results)):
        try:
            newPos = Position.objects.get(person=results[i].person, season=results[i].run.season)
            newPos.points += results[i].points
        except Position.DoesNotExist:
            newPos = Position(person=results[i].person, position_season = 0, season = results[i].run.season, position_category = 0, points = results[i].points)
        newPos.save()
    position = Position.objects.all().order_by('-points')
    categories = Category.objects.all()
    categoryPositionCursor = dict()
    for category in categories:
        categoryPositionCursor[category] = 1
    for i in range(len(position)):
        position[i].position_season = i+1
        position[i].position_category = categoryPositionCursor[position[i].person.category]
        categoryPositionCursor[position[i].person.category] += 1
        position[i].save()

def nullPoints():
    position = Position.objects.all()
    for pos in position:
        pos.points = 0
        pos.position_season = 0
        pos.position_category = 0
        pos.save()


def eval2(request):
    if request.method == 'POST':
        form = EvalForm02(request.POST)
        if form.is_valid():
            runs = form.cleaned_data['runs']
            interval = form.cleaned_data['interval']
            points_last = form.cleaned_data['points_last']
            if runs is not None:
                runs_for_calculation = Run.objects.filter(season=runs)
                for run_name in runs_for_calculation:
                    inputList = []
                    personList = Person.objects.filter(runs = Run.objects.get(pk = run_name.pk))
                    for persona in personList:
                        if Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk = run_name.pk)).status != 'OK':
                            continue
#                        time = str(unicodedata.normalize('NFKD', Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk = run_name.pk)).result_time).encode('ascii', 'ignore'))
                        time = Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk = run_name.pk)).result_time
                        seconds = int(time)
                        points = Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk = run_name.pk)).points
                        inputList.append([persona.pk, seconds, points])
                    if interval is not None and points_last is not None:
                        result = Evaluation2(inputList, interval, points_last).outputList
                        vyhodnot(result, run_name.pk)
                return HttpResponseRedirect(reverse('web:databasePerson'))
    else:
        form = EvalForm02()
    return render(request, 'web/eval2.html', {'form':form})

def eval3(request):
    if request.method == 'POST':
        form = EvalForm03(request.POST)
        if form.is_valid():
            runs = form.cleaned_data['runs']
            score = form.cleaned_data['score']
            if runs is not None:
                runs_for_calculation = Run.objects.filter(season=runs)
                for run_name in runs_for_calculation:
                    inputList = []
                    personList = Person.objects.filter(runs = Run.objects.get(pk = run_name.pk))
                    for persona in personList:
                        if Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk = run_name.pk)).status != 'OK':
                            continue
#                        time = str(unicodedata.normalize('NFKD', Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk = run_name.pk)).result_time).encode('ascii', 'ignore'))
                        time = Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk = run_name.pk)).position_run
                        seconds = int(time)
                        points = Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk = run_name.pk)).points
                        inputList.append([persona.pk, seconds, points])
                    if score:
                        score_list = score.split(',')
                        for s in range(len(score_list)):
                            score_list[s] = int(unicodedata.normalize('NFKD', score_list[s]).encode('ascii', 'ignore'))
                        result = Evaluation3(inputList, score_list).outputList
                        vyhodnot(result, run_name.pk)
                return HttpResponseRedirect(reverse('web:databasePerson'))
    else:
        form = EvalForm03()
    return render(request, 'web/eval3.html', {'form':form})

def eval4(request):
    if request.method == 'POST':
        form = EvalForm04(request.POST)
        if form.is_valid():
            runs = form.cleaned_data['runs']
            table = form.cleaned_data['table']
            new_table = table.split(',')
            if runs is not None:
                runs_for_calculation = Run.objects.filter(season=runs)
                for run_name in runs_for_calculation:
                    inputList = []
                    personList = Person.objects.filter(runs = Run.objects.get(pk=run_name.pk))
                    for persona in personList:
                        if Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk=run_name.pk)).status != 'OK':
                            continue
#                        time = str(unicodedata.normalize('NFKD', Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk=run_name.pk)).result_time).encode('ascii', 'ignore'))
#                        seconds = timeSum(time)
                        time = Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk = run_name.pk)).result_time
                        seconds = int(time)
                        points = Result.objects.get(person=Person.objects.get(pk=persona.pk), run = Run.objects.get(pk=run_name.pk)).points
                        inputList.append([persona.pk, seconds, points])
                    input_table = []
                    for row in new_table:
                        new_t = row.split('-')
                        for number in range(len(new_t)):
                            if new_t[number]:
                                new_t[number] = int(unicodedata.normalize('NFKD', new_t[number]).encode('ascii', 'ignore'))
                        input_table.append(new_t)
                    result = Evaluation4(inputList, input_table).outputList
                    vyhodnot(result, request.POST['runs'])
                return HttpResponseRedirect(reverse('web:databasePerson'))
    else:
        form = EvalForm04()
    return render(request, 'web/eval4.html', {'form':form})

def score(request):
	return render(request, 'web/score.html')

def database(request):
    season = Season.objects.all()
    club = Club.objects.all()
    category = Category.objects.all()
    run = Run.objects.all()
    person = Person.objects.all()
    result = Result.objects.all()
    position = Position.objects.all()
    document = Document.objects.all()
    return render(request, 'web/database.html', {'category': category,'season': season,'club': club,
                                                 'run': run,'person': person, 'result': result,
                                                 'position': position,'document': document})
def databasePerson(request):
    table = Person.objects.all()
    return render(request, 'web/databasePerson.html', {'table': table })
def databaseCategory(request):
    table = Category.objects.all()
    return render(request, 'web/databaseCategory.html', {'table': table })
def databaseClub(request):
    table = Club.objects.all()
    return render(request, 'web/databaseClub.html', {'table': table })
def databaseResult(request):
    table = Result.objects.all()
    return render(request, 'web/databaseResult.html', {'table': table })
def databasePosition(request):
    table = Position.objects.all()
    return render(request, 'web/databasePosition.html', {'table': table })
def databaseSeason(request):
    table = Season.objects.all()
    return render(request, 'web/databaseSeason.html', {'table': table })
def databaseRun(request):
    table = Run.objects.all()
    return render(request, 'web/databaseRun.html', {'table': table })

def export(request):
    categories = Category.objects.all()
    cat_roster = dict()
    runs = Run.objects.all()
    for cat in categories:
        cat_roster[cat] = []
        for pos_per in Position.objects.filter(person__in = Person.objects.filter(category=cat)).order_by('position_category'):
            per = pos_per.person
            run = Run.objects.all()
            res_per = {}
            for r in run:
                try:
                    res = Result.objects.get(run=r,person = per)
                    res_per[r.id] = res.points
                except Result.DoesNotExist:
                    res_per[r.id] = 0
            cat_roster[cat].append({'sum_points':pos_per.points,'per':per, 'results': res_per , 'index':pos_per.position_category})

    return render(request, 'web/export.html', {'roster':cat_roster, 'runs':runs})

def merge(request):
    data = pickle.loads(request.session['data'])
    model = pickle.loads(request.session['model'])
    if request.method == "POST":
        if str(model) == 'club':
            form = ClubForm(request.POST)
            if form.is_valid():
                newClub = Club(name = request.POST['name'])
                newClub.save()
                clubsToChange = Club.objects.filter(pk__in = data)
                runnersToChange = Person.objects.filter(club__in = clubsToChange)
                for runner in runnersToChange:
                    runner.club = newClub
                    runner.save()
                #deleting clubs which are now obsolete
                for club in clubsToChange:
                    club.delete()
            return HttpResponseRedirect(reverse('admin:index'))

        elif str(model) == 'category':
            form = CategoryForm(request.POST)
            if form.is_valid():
                newCategory = Category(name = request.POST['name'])
                newCategory.save()
                categoriesToChange = Category.objects.filter(pk__in = data)
                runnersToChange = Person.objects.filter(category__in = categoriesToChange)
                for runner in runnersToChange:
                    runner.category = newCategory
                    runner.save()
                #deleting categories which are now obsolete
                for category in categoriesToChange:
                    category.delete()
            return HttpResponseRedirect(reverse('admin:index'))

        elif str(model) == 'person':
            form = PersonForm(request.POST)
            if form.is_valid():
                newPerson = Person(first_name = request.POST['first_name'],last_name = request.POST['last_name'],category = Category.objects.get(pk=request.POST['category']),person_id = request.POST['person_id'],club= Club.objects.get(pk=request.POST['club']),ccard = request.POST['ccard'])
                newPerson.save()
                runnersToChange = Person.objects.filter(pk__in = data)
                for oldRunner in runnersToChange:
                    for oldRunnerRun in oldRunner.runs.all():
                        oldResult = Result.objects.get(person=oldRunner.pk,run = oldRunnerRun.pk)
                        renewResult = oldResult
                        renewResult.person = newPerson
                        renewResult.save()
                #deleting categories which are now obsolete
                for runner in runnersToChange:
                    runner.delete()
                return HttpResponseRedirect(reverse('admin:index'))
            return HttpResponseRedirect(reverse('web:index'))


    else:
        if str(model) == 'club':
            zoznam = Club.objects.filter(pk__in = data)
            form = ClubForm(initial={'name':zoznam[0].name, 'shortcut':zoznam[0].shortcut})
        elif str(model) == 'person':
            zoznam = Person.objects.filter(pk__in = data)
            form = PersonForm(initial={'first_name':zoznam[0].first_name,'last_name':zoznam[0].last_name, 'person_id':zoznam[0].person_id, 'club':zoznam[0].club, 'ccard':zoznam[0].ccard, 'category':zoznam[0].category})
        elif str(model) == 'category':
            zoznam = Category.objects.filter(pk__in = data)
            form = CategoryForm(initial={'name':zoznam[0].name})
    return render(request, 'web/merge.html', {'form':form,
                                              'zoznam':zoznam,
                                              })

def export_csv(request):
    people = Person.objects.values('category__name', 'position__position_category','first_name', 'last_name', 'person_id', 'position__points', 'result__points', 'runs__name')
    return render_to_csv_response(people, delimiter=str(','))
