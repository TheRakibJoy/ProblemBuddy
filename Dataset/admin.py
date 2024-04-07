from django.contrib import admin
from .models import Pupil,Specialist,Expert,Candidate_Master,Master,Counter,Handle
# Register your models here.
admin.site.register(Specialist)
admin.site.register(Expert)
admin.site.register(Pupil)
admin.site.register(Candidate_Master)
admin.site.register(Master)
admin.site.register(Counter)
admin.site.register(Handle)