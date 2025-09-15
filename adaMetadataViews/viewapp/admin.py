from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Records)
admin.site.register(SubjectSchemas)
admin.site.register(RecordSubjects)
admin.site.register(RecordTrails)
admin.site.register(RecordCreators)
admin.site.register(RecordFiles)
admin.site.register(RecordFundings)
admin.site.register(RecordContributors)
admin.site.register(RecordRelations)
admin.site.register(NameEntities)
admin.site.register(NameEntityIdentifiers)
admin.site.register(Licenses)
admin.site.register(RecordLicenses)
admin.site.register(Funders)

