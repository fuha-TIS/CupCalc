from django.db import models

# Create your models here.
class Season(models.Model):
    name = models.CharField(max_length = 128)
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return self.name

class Club(models.Model):
    name = models.CharField(max_length = 128)
    shortcut = models.CharField(max_length = 3, default = '000')
    def __unicode__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length = 25)


    def __unicode__(self):
        return self.name

class Run(models.Model):
    name = models.CharField(max_length=128)
    date = models.DateField()
    season = models.ForeignKey(Season)

    def __unicode__(self):
        return unicode(self.pk) + ", " + self.name

class Person(models.Model):
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 25)
    club = models.ForeignKey(Club)
    category = models.ForeignKey(Category)
    ccard  = models.TextField(null = True)
    person_id = models.TextField(null = True)
    runs = models.ManyToManyField(Run, through='Result')

    def __unicode__(self):
        return unicode( self.pk ) + ", " + self.first_name + " " + self.last_name


class Result(models.Model):
    person = models.ForeignKey(Person)
    run = models.ForeignKey(Run)
    start_time = models.CharField(max_length = 25,null = True)
    finish_time = models.CharField(max_length = 25,null = True)
    result_time = models.CharField(max_length = 25, null = True)
    status = models.TextField()
    points = models.DecimalField(max_digits=10,decimal_places=5)
    position_run = models.IntegerField(null = True)

    def __unicode__(self):
        return unicode( self.pk ) + ", " + self.person.first_name + ", " + self.run.name


class Position(models.Model):
    position_season = models.IntegerField()
    position_category = models.IntegerField()
    season = models.ForeignKey(Season)
    person = models.ForeignKey(Person)
    points = models.DecimalField(max_digits=10, decimal_places=5, default=0)

    def __unicode__(self):
        return unicode( self.position_season ) + ',' + unicode( self.position_category ) + ',' + unicode( self.season ) + ',' + unicode( self.person )

class Document(models.Model):
    xmlfile = models.FileField(upload_to='xml')
    season = models.ForeignKey(Season)

    def __unicode__(self):
#        return "AbsPath:" + os.path.abspath(self.xmlfile.name) + "\tBasename: " + os.path.basename(self.xmlfile.name) + "\tRealPath: " + os.path.realpath(self.xmlfile.name)
        return self.xmlfile.url
