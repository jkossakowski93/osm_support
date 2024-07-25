# Generated by Django 4.0.3 on 2022-04-27 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import oppcore.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='nazwa')),
                ('type', models.CharField(blank=True, choices=[('OPP', 'OPP'), ('Fundacja', 'Fundacja'), ('Inne', 'Inne')], max_length=20, null=True, verbose_name='typ')),
                ('address', models.CharField(max_length=100, verbose_name='adres')),
                ('email', models.CharField(max_length=100, verbose_name='e-mail')),
                ('krs_no', models.BigIntegerField(blank=True, null=True, verbose_name='numer KRS')),
                ('pl_scope', models.TextField(blank=True, max_length=1600, null=True, verbose_name='zakres działania')),
                ('en_scope', models.TextField(blank=True, max_length=1600, null=True, verbose_name='zakres działania')),
                ('uk_scope', models.TextField(blank=True, max_length=1600, null=True, verbose_name='zakres działania')),
                ('admins', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('coordinators', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)scoordinators', to='auth.group')),
            ],
        ),
        migrations.CreateModel(
            name='OppSpot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='nazwa')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='adres')),
                ('email', models.CharField(blank=True, max_length=100, null=True, verbose_name='e-mail')),
                ('phone_no_1', models.CharField(blank=True, max_length=30, null=True, verbose_name='numer telefonu 1')),
                ('phone_no_2', models.CharField(blank=True, max_length=30, null=True, verbose_name='numer telefonu 2')),
                ('geo_lat', models.DecimalField(decimal_places=8, default=0, max_digits=12, verbose_name='szerokość geo.')),
                ('geo_long', models.DecimalField(decimal_places=8, default=0, max_digits=12, verbose_name='długość geo.')),
                ('pl_description', models.TextField(blank=True, max_length=1600, null=True, verbose_name='opis punktu')),
                ('pl_spot_needs', models.TextField(blank=True, max_length=1600, null=True, verbose_name='czego punkt potrzebuje')),
                ('pl_spot_offers', models.TextField(blank=True, max_length=1600, null=True, verbose_name='co punkt oferuje')),
                ('en_description', models.TextField(blank=True, max_length=1600, null=True, verbose_name='opis punktu')),
                ('en_spot_needs', models.TextField(blank=True, max_length=1600, null=True, verbose_name='czego punkt potrzebuje')),
                ('en_spot_offers', models.TextField(blank=True, max_length=1600, null=True, verbose_name='co punkt oferuje')),
                ('uk_description', models.TextField(blank=True, max_length=1600, null=True, verbose_name='opis punktu')),
                ('uk_spot_needs', models.TextField(blank=True, max_length=1600, null=True, verbose_name='czego punkt potrzebuje')),
                ('uk_spot_offers', models.TextField(blank=True, max_length=1600, null=True, verbose_name='co punkt oferuje')),
                ('availability', models.DateTimeField(default=oppcore.models.tz_plus_30_days, verbose_name='dostępność')),
                ('status', models.CharField(blank=True, choices=[('Zweryfikowany', 'Zweryfikowany'), ('Niezweryfikowany', 'Niezweryfikowany'), ('Nieaktywny', 'Nieaktywny')], default='Niezweryfikowany', max_length=20, verbose_name='status')),
            ],
        ),
        migrations.CreateModel(
            name='OppSpotCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pl_name', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='kategoria')),
                ('en_name', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='kategoria')),
                ('uk_name', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='kategoria')),
            ],
        ),
        migrations.CreateModel(
            name='OppSpotPhotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(default='default1.jpg', upload_to='oppspot_photos')),
                ('image2', models.ImageField(default='default2.jpg', upload_to='oppspot_photos')),
                ('image3', models.ImageField(default='default3.jpg', upload_to='oppspot_photos')),
                ('oppspot', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='oppcore.oppspot')),
            ],
        ),
        migrations.CreateModel(
            name='OppSpotOpenHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mon_start', models.TimeField(blank=True, null=True, verbose_name='pon otwarcie')),
                ('mon_end', models.TimeField(blank=True, null=True, verbose_name='pon zamknięcie')),
                ('tue_start', models.TimeField(blank=True, null=True, verbose_name='wt otwarcie')),
                ('tue_end', models.TimeField(blank=True, null=True, verbose_name='wt zamknięcie')),
                ('wen_start', models.TimeField(blank=True, null=True, verbose_name='sr otwarcie')),
                ('wen_end', models.TimeField(blank=True, null=True, verbose_name='sr zamknięcie')),
                ('thu_start', models.TimeField(blank=True, null=True, verbose_name='czw otwarcie')),
                ('thu_end', models.TimeField(blank=True, null=True, verbose_name='czw zamknięcie')),
                ('fri_start', models.TimeField(blank=True, null=True, verbose_name='pt otwarcie')),
                ('fri_end', models.TimeField(blank=True, null=True, verbose_name='pt zamknięcie')),
                ('sat_start', models.TimeField(blank=True, null=True, verbose_name='sob otwarcie')),
                ('sat_end', models.TimeField(blank=True, null=True, verbose_name='sob zamknięcie')),
                ('sun_start', models.TimeField(blank=True, null=True, verbose_name='nie otwarcie')),
                ('sun_end', models.TimeField(blank=True, null=True, verbose_name='nie zamknięcie')),
                ('oppspot', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='oppcore.oppspot')),
            ],
        ),
        migrations.AddField(
            model_name='oppspot',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oppcore.oppspotcategory'),
        ),
        migrations.AddField(
            model_name='oppspot',
            name='opp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oppcore.opp'),
        ),
        migrations.CreateModel(
            name='OppHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='ostatnio zmodyfikowano')),
                ('modification_type', models.CharField(blank=True, max_length=100, null=True)),
                ('opp', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='oppcore.opp')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
