from django import forms
from .models import Opp, OppSpot, OppSpotCategory, OppSpotPhotos, OppSpotOpenHours
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, MultiField, Div, Fieldset, ButtonHolder, Submit


class UserRegisterForm(UserCreationForm):
    #email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2'] # 'email',

class OppUpdateForm_PL(forms.ModelForm):

    class Meta:
        model = Opp
        fields = ['name', 'type', 'krs_no', 'address', 'email', 'pl_scope']

class OppUpdateForm_EN(forms.ModelForm):

    class Meta:
        model = Opp
        fields = ['name', 'type', 'krs_no', 'address', 'email', 'en_scope']

class OppUpdateForm_UK(forms.ModelForm):

    class Meta:
        model = Opp
        fields = ['name', 'type', 'krs_no', 'address', 'email', 'uk_scope']

class OppTranslateForm_PL(forms.ModelForm):

    class Meta:
        model = Opp
        fields = ['pl_scope']

class OppTranslateForm_EN(forms.ModelForm):

    class Meta:
        model = Opp
        fields = ['en_scope']

class OppTranslateForm_UK(forms.ModelForm):

    class Meta:
        model = Opp
        fields = ['uk_scope']

class OppSpotUpdateForm_PL(forms.ModelForm):

    class Meta:
        model = OppSpot
        fields = ['name', 'address', 'category', 'phone_no_1', 'phone_no_2', 'email',
            'pl_description', 'pl_spot_needs', 'pl_spot_offers', 'availability', 'status','geo_lat', 'geo_long',]

class OppSpotUpdateForm_EN(forms.ModelForm):

    class Meta:
        model = OppSpot
        fields = ['name', 'address', 'category', 'phone_no_1', 'phone_no_2', 'email',
            'en_description', 'en_spot_needs', 'en_spot_offers', 'availability', 'status','geo_lat', 'geo_long',]

class OppSpotUpdateForm_UK(forms.ModelForm):

    class Meta:
        model = OppSpot
        fields = ['name', 'address', 'category', 'phone_no_1', 'phone_no_2', 'email',
            'uk_description', 'uk_spot_needs', 'uk_spot_offers', 'availability', 'status','geo_lat', 'geo_long',]

class AddOppSpotCategory_PL(forms.ModelForm):

    class Meta:
        model = OppSpotCategory
        fields = ['pl_name']

class AddOppSpotCategory_EN(forms.ModelForm):

    class Meta:
        model = OppSpotCategory
        fields = ['en_name']

class AddOppSpotCategory_UK(forms.ModelForm):

    class Meta:
        model = OppSpotCategory
        fields = ['uk_name']

class AddPhotosToOppSpot(forms.ModelForm):

    class Meta:
        model = OppSpotPhotos
        fields = ['image1','image2','image3']

class Row(Div):
    css_class = "form-column"

class AddOppSpotOpenHours(forms.ModelForm):

    class Meta:
        model = OppSpotOpenHours
        fields = ['mon_start','mon_end','tue_start','tue_end','wen_start','wen_end','thu_start',
                  'thu_end','fri_start','fri_end','sat_start','sat_end','sun_start','sun_end']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Div(
    #             Field('mon_start', wrapper_class='col-md-3'),
    #             Field('mon_end', wrapper_class='col-md-3'),
    #             Field('fri_start', wrapper_class='col-md-3'),
    #             css_class='form-row'),
    #         Div(
    #             Field('tue_start', wrapper_class='col-md-3'),
    #             Field('tue_end', wrapper_class='col-md-3'),
    #             css_class='form-row'),
    #         # Div(
    #         #     Div('mon_start', css_class='span6'),
    #         #     Div('mon_end', css_class='span6'),
    #         #     css_class='row-fluid'),
    #         # Div(
    #         #     Div('tue_start', css_class='span6'),
    #         #     Div('tue_end', css_class='span6'),
    #         #     css_class='row-fluid'),
    #     )



        # )
        #     ButtonHolder(
        #         Submit('submit', 'Submit', css_class='button white')
        #     )
        # )


    # category = forms.ChoiceField(choices=[
    #     (each.id, each) for each in OppSpotCategory.objects.all()
    # ], widget=forms.TextInput(attrs={'class': "form-control"}))