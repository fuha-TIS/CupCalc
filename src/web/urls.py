from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^runs/$', views.runs, name='runs'),
    url(r'^runs/parse/(?P<documentPk>\d+)/$', views.parse, name='parse'),
    url(r'^export/$', views.export, name='export'),
    url(r'^export/csv$', views.export_csv, name='export_csv'),
    url(r'^database/$', views.database, name='database'),
    url(r'^database/person$', views.databasePerson, name='databasePerson'),
    url(r'^database/club$', views.databaseClub, name='databaseClub'),
    url(r'^database/category$', views.databaseCategory, name='databaseCategory'),
    url(r'^database/position$', views.databasePosition, name='databasePosition'),
    url(r'^database/result$', views.databaseResult, name='databaseResult'),
    url(r'^database/season$', views.databaseSeason, name='databaseSeason'),
    url(r'^database/run$', views.databaseRun, name='databaseRun'),
    url(r'^score/$', views.score, name='score'),
    url(r'^score/eval1/$', views.eval1, name='eval1'),
    url(r'^score/eval2/$', views.eval2, name='eval2'),
    url(r'^score/eval3/$', views.eval3, name='eval3'),
    url(r'^score/eval4/$', views.eval4, name='eval4'),
]
