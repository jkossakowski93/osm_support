from unicodedata import category
from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, User
# from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _
from PIL import Image


# if 'global_coords' not in Group.objects.all().values_list('name', flat = True):
#     g = Group(name = 'global_coords')
#     g.save()

# class OppUser(AbstractUser):
#     # """User class for purpose of this project is augmented by usergroup field - we want to have it in forms"""
#     # usergroup = models.CharField(max_length=20, choices=[('AdminOPP', 'AdminOPP'), ('CoordinatorOPP', 'CoordinatorOPP')],
#     #                          default='CoordinatorOPP')
#     pass

# class AdminGroup(Group):
#
#     class Meta:
#         proxy = True
#
# class CoordinatorGroup(Group):
#     class Meta:
#         proxy = True

class Opp(models.Model):
    """
    Contains all information about OPP registered in system
    OPP is from polish 'Organizacja Pożytku Publicznego',
    that means 'public benefit organization'.
    """

    name = models.CharField(_('nazwa'), max_length=100, unique=True)
    type = models.CharField(_('typ'), max_length=20, null = True, blank = True,
                              choices=[('OPP', _('OPP')), ('Fundacja', _('Fundacja')), ('Inne', _('Inne'))],
                              )
    address = models.CharField(_('adres'), max_length=100)
    email = models.CharField(_('e-mail'), max_length=100)
    krs_no = models.BigIntegerField(_('numer KRS'), null = True, blank = True)
    admins = models.ForeignKey(Group, on_delete=models.CASCADE, null = True, blank = True) # to jest źle... powinna być zdefiniowana grupa AdminGroup ktora dziedziczy z Grupy i ma relacje one to one z OPP. Wtedy przy usuwaniu OPPA grupy bbylyby usuwane automatycznie, a tak nie są...
    coordinators = models.OneToOneField(Group, on_delete=models.CASCADE, null = True, blank = True, related_name='%(class)scoordinators') # jw.
    #scope = models.TextField(_('scope'), max_length=1600, null=True, blank=True)
    pl_scope = models.TextField('zakres działania', default='<nie przetłumaczono>', max_length=1600, null=True, blank=True)
    en_scope = models.TextField('scope of activities', default='<to be translated>', max_length=1600, null=True, blank=True)
    uk_scope = models.TextField('діапазон діяльності', default='<ukr nie przetłumaczono>', max_length=1600, null=True, blank=True)

    # history = HistoricalRecords()

    def __str__(self):
        return str(self.name)


class OppHistory(models.Model):
    """Contains logs of all changes of OPP"""
    opp = models.OneToOneField(Opp, on_delete = models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)  # edited by who?
    last_modified = models.DateTimeField(_('ostatnio zmodyfikowano'), default=timezone.now)  # and when
    modification_type = models.CharField(max_length=100, blank=True, null=True) # we will fill this automatically, based on what was modified, but we enforce on admin to fill this message when he tried to delete an OPP

    def __str__(self):
        return str(str(self.opp) + _(' Przez ') + str(self.user) + _(' Dnia ') + str(self.last_modified))


class OppSpotCategory(models.Model):

    # name = models.CharField(_('kategoria'), max_length=100, unique=True)
    pl_name = models.CharField('kategoria', max_length=100, unique=True, blank=True, null=True)
    en_name = models.CharField('category', max_length=100, unique=True, blank=True, null=True)
    uk_name = models.CharField('категорія', max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return str(self.pl_name)

def tz_plus_30_days():
    return timezone.now() + timezone.timedelta(days=7)

class OppSpot(models.Model):
    """Contains information about a spot where OPP operates/collects"""
    opp = models.ForeignKey(Opp, on_delete = models.CASCADE)
    name = models.CharField(_('nazwa'), max_length=200, null=True)
    address = models.CharField(_('adres'), max_length=100, blank=True, null=True)
    email = models.CharField(_('e-mail'), max_length=100, blank=True, null=True)
    phone_no_1 = models.CharField(_('numer telefonu 1'), max_length=30, blank=True, null=True)
    phone_no_2 = models.CharField(_('numer telefonu 2'), max_length=30, blank=True, null=True)
    geo_lat = models.DecimalField(_('szerokość geo.'), max_digits=12, decimal_places=8, default = 0)
    geo_long = models.DecimalField(_('długość geo.'), max_digits=12, decimal_places=8, default = 0)
    #description = models.TextField(_('description'), max_length=1600, blank=True, null=True)
    # spot_needs = models.TextField(_('spot_needs'), max_length=1600, blank=True, null=True)
    # spot_offers = models.TextField(_('spot_offers'), max_length=1600, blank=True, null=True)
    pl_description = models.TextField(_('opis punktu'), max_length=1600, blank=True, null=True)
    pl_spot_needs = models.TextField(_('czego punkt potrzebuje'), max_length=1600, blank=True, null=True)
    pl_spot_offers = models.TextField(_('co punkt oferuje'), max_length=1600, blank=True, null=True)
    en_description = models.TextField(_('opis punktu'), max_length=1600, blank=True, null=True)
    en_spot_needs = models.TextField(_('czego punkt potrzebuje'), max_length=1600, blank=True, null=True)
    en_spot_offers = models.TextField(_('co punkt oferuje'), max_length=1600, blank=True, null=True)
    uk_description = models.TextField(_('opis punktu'), max_length=1600, blank=True, null=True)
    uk_spot_needs = models.TextField(_('czego punkt potrzebuje'), max_length=1600, blank=True, null=True)
    uk_spot_offers = models.TextField(_('co punkt oferuje'), max_length=1600, blank=True, null=True)
    availability = models.DateTimeField(_('dostępność'), default = tz_plus_30_days)
    status = models.CharField(_('status'), max_length=20, blank=True,
                              choices=[('Zweryfikowany', _('Zweryfikowany')), ('Niezweryfikowany', _('Niezweryfikowany')), ('Nieaktywny', _('Nieaktywny'))],
                              default='Niezweryfikowany')
    category = models.ForeignKey(OppSpotCategory, on_delete=models.SET_NULL ,blank = True, null = True)
    # history = HistoricalRecords()

    def __str__(self):
        return str(self.opp.name + ' - ' + self.name)



class OppSpotPhotos(models.Model):

    oppspot = models.OneToOneField(OppSpot, on_delete=models.CASCADE)
    image1 = models.ImageField(default='default1.jpg', upload_to='oppspot_photos')
    image2 = models.ImageField(default='default2.jpg', upload_to='oppspot_photos')
    image3 = models.ImageField(default='default3.jpg', upload_to='oppspot_photos')

    def __str__(self):
        return f'Zdjecia {self.oppspot.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img1 = Image.open(self.image1.path)
        img2 = Image.open(self.image2.path)
        img3 = Image.open(self.image3.path)

        for img, path in zip([img1, img2, img3], [self.image1.path, self.image2.path, self.image3.path]):

            if img.height > 500 or img.width > 500:
                Max_size = (500, 500)
                img.thumbnail(Max_size)
                img.save(path)

            else:
                del img

class OppSpotOpenHours(models.Model):

    oppspot = models.OneToOneField(OppSpot, on_delete=models.CASCADE)
    mon_start = models.TimeField(_('pon otwarcie'), null = True, blank = True)
    mon_end = models.TimeField(_('pon zamknięcie'), null = True, blank = True)
    tue_start = models.TimeField(_('wt otwarcie'), null=True, blank=True)
    tue_end = models.TimeField(_('wt zamknięcie'), null=True, blank=True)
    wen_start = models.TimeField(_('sr otwarcie'), null=True, blank=True)
    wen_end = models.TimeField(_('sr zamknięcie'), null=True, blank=True)
    thu_start = models.TimeField(_('czw otwarcie'), null=True, blank=True)
    thu_end = models.TimeField(_('czw zamknięcie'), null=True, blank=True)
    fri_start = models.TimeField(_('pt otwarcie'), null=True, blank=True)
    fri_end = models.TimeField(_('pt zamknięcie'), null=True, blank=True)
    sat_start = models.TimeField(_('sob otwarcie'), null=True, blank=True)
    sat_end = models.TimeField(_('sob zamknięcie'), null=True, blank=True)
    sun_start = models.TimeField(_('nie otwarcie'), null=True, blank=True)
    sun_end = models.TimeField(_('nie zamknięcie'), null=True, blank=True)

