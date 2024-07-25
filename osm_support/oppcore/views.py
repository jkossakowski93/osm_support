from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate
from .models import Opp, OppHistory, OppSpot, OppSpotCategory, OppSpotPhotos, OppSpotOpenHours
from.forms import UserRegisterForm, OppUpdateForm_PL, OppUpdateForm_EN, OppUpdateForm_UK, \
    OppTranslateForm_PL, OppTranslateForm_EN, OppTranslateForm_UK, \
    OppSpotUpdateForm_PL, OppSpotUpdateForm_EN, OppSpotUpdateForm_UK, AddOppSpotCategory_PL, \
    AddOppSpotCategory_EN, AddOppSpotCategory_UK, AddPhotosToOppSpot, AddOppSpotOpenHours


@login_required
def home(request):

    if request.user.is_superuser or request.user.groups.filter(name='global_coords').exists():
        return redirect('home_global_coordinator')
    else:
        return redirect('home_local_coordinator')

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='global_coords').exists())
def home_global_coordinator(request):

    current_lang = request.LANGUAGE_CODE

    context = {
        'data_url': f"/{current_lang}/json_for_global_coordinator",
        # 'Nazwa OPP': _('Nazwa OPP'),
        # 'Adres': _('Adres'),
        # 'E-mail': _('E-mail'),
        # 'Zakres działania': _('Zakres działania'),
    }

    return render(request, 'oppcore/home_global_coordinator.html', context)

@login_required
def home_local_coordinator(request):

    current_lang = request.LANGUAGE_CODE

    context = {
        'data_url': f"/{current_lang}/json_for_local_coordinator",
        # 'Nazwa OPP': _('Nazwa OPP'),
        # 'Adres': _('Adres'),
        # 'E-mail': _('E-mail'),
        # 'Zakres działania': _('Zakres działania'),
    }

    return render(request, 'oppcore/home_global_coordinator.html', context)

@login_required
def opp_details(request, opp_id):

    opp = get_object_or_404(Opp, pk=opp_id)

    if len(OppHistory.objects.filter(opp_id = opp_id)) == 0: #długość querysetu
        opphistory = None
    else: #długość querysetu
        opphistory = OppHistory.objects.filter(opp_id = opp_id).order_by('-date_uploaded')[0]
    #
    # if len(AuscDownloadHistory.objects.filter(ausc_id = ausc_id)) == 0: #długość querysetu
    #     auscdownhist = None
    # else: #długość querysetu
    #     auscdownhist = AuscDownloadHistory.objects.filter(ausc_id = ausc_id).order_by('-date_downloaded')[0]

    # if ausc.file:
    #     plot_spectogram(ausc.file)
    # if ausc.file_url:
    #     with open(os.path.join(settings.MEDIA_ROOT, 'temp_from_db.wav'), 'wb') as f:
    #         f.write(requests.get(ausc.file_url).content)
    #     plot_spectogram(os.path.join(settings.MEDIA_ROOT, 'temp_from_db.wav'))

    context = {'opp': opp, 'opphistory': opphistory, 'data_url': f"/{opp_id}/json_for_opp_points",
               '1_bool': request.user.groups.filter(name='global_coords').exists() }

    # return render(request, 'sthetocad/detail.html', {'ausc': ausc,} )
    return render(request, 'oppcore/opp_details.html', context) # {'ausc': ausc.file.url}

@login_required
@user_passes_test(lambda u: u.is_superuser) #  or u.groups.filter(name='global_coords').exists()
def register_global_coordinator(request):

    if request.method == 'POST':

        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _('Globalny koordynator został pomyślnie zarejestrowany!'))
            user = User.objects.get(username = username)
            group = Group.objects.get(name='global_coords')
            user.groups.add(group)
            return redirect('home')
        # else:
    else:
        if 'global_coords' not in Group.objects.all().values_list('name', flat = True):
            g = Group(name = 'global_coords')
            g.save()
        user = User()

        form = UserRegisterForm(instance = user)
        #form.fields['usergroup'].disabled = True

    return render(request, 'oppcore/register_user.html', {'form':form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def register_global_admin(request):

    if request.method == 'POST':

        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _('Globalny admin został pomyślnie zarejestrowany!'))
            user = User.objects.get(username = username)
            group = Group.objects.get(name='global_coords')
            user.groups.add(group)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            return redirect('home')
        # else:
    else:
        if 'global_coords' not in Group.objects.all().values_list('name', flat = True):
            g = Group(name = 'global_coords')
            g.save()
        user = User()

        form = UserRegisterForm(instance = user)
        #form.fields['usergroup'].disabled = True

    return render(request, 'oppcore/register_user.html', {'form':form})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='global_coords').exists()) #  or u.groups.filter(name='global_coords').exists()
def register_local_coordinator(request, opp_id):

    if request.method == 'POST':

        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _('Lokalny koordynator został pomyślnie zarejestrowany!'))
            user = User.objects.get(username = username)
            #group = Group.objects.get(name='global_coords')
            opp = Opp.objects.get(pk = opp_id)
            user.groups.add(opp.coordinators)
            return redirect('opp_details', opp_id)
        # else:
    else:
        if 'global_coords' not in Group.objects.all().values_list('name', flat = True):
            g = Group(name = 'global_coords')
            g.save()
        user = User()

        form = UserRegisterForm(instance = user)
        #form.fields['usergroup'].disabled = True

    return render(request, 'oppcore/register_user.html', {'form':form})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='global_coords').exists())
def register_local_admin(request, opp_id):

    if request.method == 'POST':

        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _('Lokalny admin został pomyślnie zarejestrowany!'))
            user = User.objects.get(username = username)
            # group = Group.objects.get(name='global_coords')
            opp = Opp.objects.get(pk=opp_id)
            user.groups.add(opp.admins)
            user.groups.add(opp.coordinators)
            return redirect('opp_details', opp_id)
        # else:
    else:
        if 'global_coords' not in Group.objects.all().values_list('name', flat = True):
            g = Group(name = 'global_coords')
            g.save()
        user = User()

        form = UserRegisterForm(instance = user)
        #form.fields['usergroup'].disabled = True

    return render(request, 'oppcore/register_user.html', {'form':form})


@login_required
def add_opp(request):

    current_lang = request.LANGUAGE_CODE

    opp = Opp()

    if request.method == 'POST':

        if current_lang == 'pl':
            form = OppUpdateForm_PL(request.POST, instance=opp)
        elif current_lang == 'en':
            form = OppUpdateForm_EN(request.POST, instance=opp)
        elif current_lang == 'uk':
            form = OppUpdateForm_UK(request.POST, instance=opp)

        if form.is_valid():

            # my_id = opp.id
            my_name = form.cleaned_data.get('name')
            form.save()

            opp = Opp.objects.get(name = my_name)
            if f'{my_name}_admins' not in Group.objects.all().values_list('name', flat=True):
                g1 = Group(name=f'{my_name}_admins')
            else:
                g1 = Group.objects.filter(name=f'{my_name}_admins').all()[0]

            if f'{my_name}_coords' not in Group.objects.all().values_list('name', flat=True):
                g2 = Group(name=f'{my_name}_coords')
            else:
                g2 = Group.objects.filter(name=f'{my_name}_coords').all()[0]

            opp.admins = g1
            opp.coordinators = g2
            g1.save()
            g2.save()
            opp.save()

            messages.success(request, 'Dodano nową organizację')
            return redirect('home')

    else:
        if current_lang == 'pl':
            form = OppUpdateForm_PL(instance=opp)
        elif current_lang == 'en':
            form = OppUpdateForm_EN(instance=opp)
        elif current_lang == 'uk':
            form = OppUpdateForm_UK(instance=opp)


    return render(request, 'oppcore/add_opp.html', {'form':form})

@login_required
def edit_opp(request, opp_id):

    current_lang = request.LANGUAGE_CODE
    opp = get_object_or_404(Opp, pk=opp_id)

    if request.method == 'POST':

        if current_lang == 'pl':
            form = OppUpdateForm_PL(request.POST, instance=opp)
            t_form_1 = OppTranslateForm_EN(request.POST, instance=opp)
            t_form_2 = OppTranslateForm_UK(request.POST, instance=opp)
        elif current_lang == 'en':
            form = OppUpdateForm_EN(request.POST, instance=opp)
            t_form_1 = OppTranslateForm_EN(request.POST, instance=opp)
            t_form_2 = OppTranslateForm_UK(request.POST, instance=opp)
        elif current_lang == 'uk':
            form = OppUpdateForm_UK(request.POST, instance=opp)
            t_form_1 = OppTranslateForm_EN(request.POST, instance=opp)
            t_form_2 = OppTranslateForm_UK(request.POST, instance=opp)

        if form.is_valid() and t_form_1.is_valid() and t_form_2.is_valid():
            form.save()
            t_form_1.save()
            t_form_2.save()
            messages.success(request, _('Edytowano organizację'))
            return redirect('opp_details', opp_id)

    else:
        if current_lang == 'pl':
            form = OppUpdateForm_PL(instance=opp)
            t_form_1 = OppTranslateForm_EN(instance=opp)
            t_form_2 = OppTranslateForm_UK(instance=opp)
        elif current_lang == 'en':
            form = OppUpdateForm_EN(instance=opp)
            t_form_1 = OppTranslateForm_PL(instance=opp)
            t_form_2 = OppTranslateForm_UK(instance=opp)
        elif current_lang == 'uk':
            form = OppUpdateForm_UK(instance=opp)
            t_form_1 = OppTranslateForm_PL(instance=opp)
            t_form_2 = OppTranslateForm_EN(instance=opp)

    return render(request, 'oppcore/edit_opp.html', {'form':form,'t_form_1':t_form_1,'t_form_2':t_form_2})

@login_required
def add_opp_spot(request, opp_id):

    current_lang = request.LANGUAGE_CODE

    opp = Opp(pk = opp_id)
    oppspot = OppSpot(opp = opp, status = 'Unverified')
    oppspotphotos = OppSpotPhotos(oppspot = oppspot)
    oppspotopenhours = OppSpotOpenHours(oppspot = oppspot)

    if request.method == 'POST':

        if current_lang == 'pl':
            form = OppSpotUpdateForm_PL(request.POST, instance=oppspot)
        elif current_lang == 'en':
            form = OppSpotUpdateForm_EN(request.POST, instance=oppspot)
        elif current_lang == 'uk':
            form = OppSpotUpdateForm_UK(request.POST, instance=oppspot)

        p_form = AddPhotosToOppSpot(request.POST, request.FILES, instance = oppspotphotos)
        h_form = AddOppSpotOpenHours(request.POST, instance = oppspotopenhours)

        if form.is_valid() and p_form.is_valid() and h_form.is_valid():
            form.save()
            p_form.save()
            h_form.save()
            messages.success(request, 'Dodano nowy punkt pomocy do organizacji')
            return redirect('opp_details', opp_id)

    else:
        if current_lang == 'pl':
            form = OppSpotUpdateForm_PL(instance=oppspot)
        elif current_lang == 'en':
            form = OppSpotUpdateForm_EN(instance=oppspot)
        elif current_lang == 'uk':
            form = OppSpotUpdateForm_UK(instance=oppspot)
        p_form = AddPhotosToOppSpot(instance = oppspotphotos)
        h_form = AddOppSpotOpenHours(instance = oppspotopenhours)
        form.fields['status'].disabled = True

    return render(request, 'oppcore/add_opp_spot.html', {'form':form,'p_form':p_form,'h_form':h_form})


@login_required
def edit_opp_spot(request, opp_id, oppspot_id):

    current_lang = request.LANGUAGE_CODE

    opp = get_object_or_404(Opp, pk=opp_id)
    oppspot = get_object_or_404(OppSpot, opp=opp, pk=oppspot_id)
    oppspotphotos = OppSpotPhotos.objects.filter(oppspot=oppspot).all()[0]
    oppspotopenhours = OppSpotOpenHours.objects.filter(oppspot=oppspot).all()[0]

    if request.method == 'POST':

        if current_lang == 'pl':
            form = OppSpotUpdateForm_PL(request.POST, instance=oppspot)
        elif current_lang == 'en':
            form = OppSpotUpdateForm_EN(request.POST, instance=oppspot)
        elif current_lang == 'uk':
            form = OppSpotUpdateForm_UK(request.POST, instance=oppspot)
        p_form = AddPhotosToOppSpot(request.POST, request.FILES, instance = oppspotphotos)
        h_form = AddOppSpotOpenHours(request.POST, instance=oppspotopenhours)

        if form.is_valid() and p_form.is_valid() and h_form.is_valid():
            form.save()
            p_form.save()
            h_form.save()
            messages.success(request, 'Edytowano punkt pomocy')
            return redirect('opp_details', opp_id)

    else:
        if current_lang == 'pl':
            form = OppSpotUpdateForm_PL(instance=oppspot)
        elif current_lang == 'en':
            form = OppSpotUpdateForm_EN(instance=oppspot)
        elif current_lang == 'uk':
            form = OppSpotUpdateForm_UK(instance=oppspot)
        p_form = AddPhotosToOppSpot(instance = oppspotphotos)

    return render(request, 'oppcore/add_opp_spot.html', {'form':form,'p_form':p_form,'h_form':h_form})

@login_required
def add_opp_spot_category(request):

    current_lang = request.LANGUAGE_CODE
    oppspotcat = OppSpotCategory()

    if request.method == 'POST':

        if current_lang == 'pl':
            form = AddOppSpotCategory_PL(request.POST, instance = oppspotcat)
        elif current_lang == 'en':
            form = AddOppSpotCategory_EN(request.POST, instance = oppspotcat)
        elif current_lang == 'uk':
            form = AddOppSpotCategory_UK(request.POST, instance = oppspotcat)


        if form.is_valid():
            form.save()
            messages.success(request, 'Dodano nową kategorię punktu pomocy')
            return redirect('home') # atm go to home, but we will change it

    else:
        if current_lang == 'pl':
            form = AddOppSpotCategory_PL()
        elif current_lang == 'en':
            form = AddOppSpotCategory_EN()
        elif current_lang == 'uk':
            form = AddOppSpotCategory_UK()


    return render(request, 'oppcore/add_opp_spot_category.html', {'form':form})

@login_required
def opp_spot_details(request, opp_id, oppspot_id):

    opp = get_object_or_404(Opp, pk=opp_id)
    oppspot = get_object_or_404(OppSpot, opp = opp, pk=oppspot_id)
    oppspotphotos = OppSpotPhotos.objects.filter(oppspot=oppspot).all()[0]

    #
    # if len(AuscDownloadHistory.objects.filter(ausc_id = ausc_id)) == 0: #długość querysetu
    #     auscdownhist = None
    # else: #długość querysetu
    #     auscdownhist = AuscDownloadHistory.objects.filter(ausc_id = ausc_id).order_by('-date_downloaded')[0]

    context = {'oppspot': oppspot, 'opp_id':opp_id, 'oppspot_id':oppspot_id, 'oppspotphotos':oppspotphotos}

    # return render(request, 'sthetocad/detail.html', {'ausc': ausc,} )
    return render(request, 'oppcore/oppspot_details.html', context) # {'ausc': ausc.file.url}


@login_required
def json_for_global_coordinator(request):
    if request.method == 'GET':

        current_lang = request.LANGUAGE_CODE
        opps = Opp.objects.all()

        #auscs = list(auscs.values('pk', 'name','date_uploaded', 'field_doc_name','status'))

        data = []
        for query in opps:
            if current_lang == 'pl':
                data.append({"pk": query.id, "name": query.name, "address": query.address, "email": query.email, 'scope':query.pl_scope })
            elif current_lang == 'en':
                data.append({"pk": query.id, "name": query.name, "address": query.address, "email": query.email, 'scope':query.en_scope })
            elif current_lang == 'uk':
                data.append({"pk": query.id, "name": query.name, "address": query.address, "email": query.email, 'scope':query.uk_scope })

        data = {'data': data}
        return JsonResponse(data)

@login_required
def json_for_local_coordinator(request):
    if request.method == 'GET':

        #opps = Opp.objects.filter(group = request.user...)all()
        #auscs = list(auscs.values('pk', 'name','date_uploaded', 'field_doc_name','status'))
        current_lang = request.LANGUAGE_CODE
        data = []

        for group in request.user.groups.all():

            if group == 'global_coords':
                continue

            opps = Opp.objects.filter(coordinators=group).all()

            for query in opps:

                if current_lang == 'pl':
                    data.append({"pk": query.id, "name": query.name, "address": query.address, "email": query.email,
                                 'scope': query.pl_scope})
                elif current_lang == 'en':
                    data.append({"pk": query.id, "name": query.name, "address": query.address, "email": query.email,
                                 'scope': query.en_scope})
                elif current_lang == 'uk':
                    data.append({"pk": query.id, "name": query.name, "address": query.address, "email": query.email,
                                 'scope': query.uk_scope})

        data = {'data': data}
        return JsonResponse(data)

@login_required
def json_for_opp_points(request, opp_id):
    if request.method == 'GET':

        current_lang = request.LANGUAGE_CODE
        oppspots = OppSpot.objects.filter(opp_id = opp_id).all()

        data = []
        for query in oppspots:
            if current_lang == 'pl':
                data.append({"pk":query.id, "name":query.name, "category":query.category.pl_name, "address":query.address,
                             "phone_no":query.phone_no_1, "spot_needs": query.pl_spot_needs, "spot_offers":query.pl_spot_offers,
                             "status":query.status, "availability": query.availability.strftime("%Y/%m/%d %H:%M:%S")
                             })
            elif current_lang == 'en':
                data.append({"pk":query.id, "name":query.name, "category":query.category.en_name, "address":query.address,
                             "phone_no":query.phone_no_1, "spot_needs": query.en_spot_needs, "spot_offers":query.en_spot_offers,
                             "status":query.status, "availability": query.availability.strftime("%Y/%m/%d %H:%M:%S")
                             })
            elif current_lang == 'uk':
                data.append({"pk":query.id, "name":query.name, "category":query.category.uk_name, "address":query.address,
                             "phone_no":query.phone_no_1, "spot_needs": query.uk_spot_needs, "spot_offers":query.uk_spot_offers,
                             "status":query.status, "availability": query.availability.strftime("%Y/%m/%d %H:%M:%S")
                             })

        data = {'data': data}
        return JsonResponse(data)

#
# @login_required
# @user_passes_test(lambda u: u.is_superuser or u.usergroup == 'AdminOPP')
# def add_opp(request):
#
#     if request.method == 'POST':
#         if request.user.usergroup == 'AdminOPP':
#             oppuser = OppUser(usergroup = 'CoordinatorOPP')
#             form = OppUserRegisterForm(instance = oppuser)
#         else:
#             form = OppUserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             #username = form.cleaned_data.get('username')
#             messages.success(request, 'Your account has been created! Use these credentials now to log in.')
#             return redirect('login')
#         # else:
#     else:
#         if request.user.usergroup == 'AdminOPP':
#             oppuser = OppUser(usergroup = 'CoordinatorOPP')
#             form = OppUserRegisterForm(instance = oppuser)
#             form.fields['usergroup'].disabled = True
#         else:
#             form = OppUserRegisterForm()
#
#     return render(request, 'oppcore/register_user.html', {'form':form})

