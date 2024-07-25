from django.contrib import admin
#from simple_history.admin import SimpleHistoryAdmin

from oppcore.models import Opp, OppSpot, OppHistory, OppSpotCategory, OppSpotPhotos, OppSpotOpenHours


admin.site.register(Opp)
admin.site.register(OppSpot)
admin.site.register(OppHistory)
admin.site.register(OppSpotCategory)
admin.site.register(OppSpotPhotos)
admin.site.register(OppSpotOpenHours)

