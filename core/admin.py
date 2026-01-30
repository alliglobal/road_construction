
from django.contrib import admin
from .models import (
    Project,
    WorkItem,
    DailyLog,
    DailyLogImage,
    Material,
    WarehouseTransaction,
    MaterialNorm
)

admin.site.register(Project)
admin.site.register(WorkItem)
admin.site.register(DailyLog)
admin.site.register(DailyLogImage)
admin.site.register(Material)
admin.site.register(WarehouseTransaction)
admin.site.register(MaterialNorm)
