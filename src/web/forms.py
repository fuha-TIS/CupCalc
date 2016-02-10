from django import forms
from web.models import Season, Run
from models import Club, Category, Person

CHOICES=[
    ('p1','Determine points of winner by number of participating counting runners'),
    ('p2','Determine points of winner by numbet of participating teams * maximum counting runners per team')
]

class EvalForm01(forms.Form):
    runs = forms.ModelChoiceField(label="Choose a season*",required=True,
                                             queryset = Season.objects.all(),
                                             widget=forms.Select())
    value = forms.IntegerField(min_value=1, max_value=500, required=False)
    value2 = forms.IntegerField(min_value=1, max_value=500, required=False)
    first = forms.IntegerField(min_value=1, max_value=2000, required=False)
    last = forms.IntegerField(min_value=1, max_value=1000, required=False)
    percents = forms.IntegerField(min_value=1, max_value=100, required=False)

class EvalForm02(forms.Form):
    runs = forms.ModelChoiceField(label="Choose a season*",required=True,
                                             queryset = Season.objects.all(),
                                             widget=forms.Select())
    interval = forms.IntegerField(min_value=1, max_value=500, label='Point interval')
    points_last = forms.IntegerField(min_value=0, max_value=200, label='Points given to last runner')
    #counting = forms.IntegerField(min_value=1, max_value=100000, label='Counting runners per club')
    #type = forms.ChoiceField(choices=CHOICES, widget = forms.RadioSelect())
    #disqualified = forms.BooleanField(label='Disqualified runners count for other runners points')

class EvalForm03(forms.Form):
    runs = forms.ModelChoiceField(label="Choose a season*",required=True,
                                             queryset = Season.objects.all(),
                                             widget=forms.Select())
    score = forms.CharField(max_length=100)

class EvalForm04(forms.Form):
    runs = forms.ModelChoiceField(label="Choose a season*",required=True,
                                             queryset = Season.objects.all(),
                                             widget=forms.Select())
    table = forms.CharField(max_length=100)

class ChooseSeasonForm(forms.Form):
    seasons = Season.objects.all()
    choose_season = forms.ChoiceField(enumerate(seasons), widget = forms.Select(), label="Choose a season")

class UploadRun(forms.Form):
    season = forms.ModelChoiceField(label="Choose a season",required=False,
                                             queryset = Season.objects.all(),
                                             widget=forms.Select())
    xml_file = forms.FileField(label="Choose a file", help_text='max. 10 megabytes')

class CreateSeason(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['name', 'start_date', 'end_date']
        labels = {
            'name': ('Name of the season'),
            'start_date': ('Start date of the season'),
            'end_date': ('End date of the season'),
        }
        help_texts = {
            'start_date': ('Date format: YYYY-MM-DD'),
        }

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'club', 'category', 'ccard', 'person_id']
