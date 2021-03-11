from django.contrib import admin
from finance.models import Stock,Detail,DisplaySr,DisplayMo,StockCorrelation
# Register your models here.

admin.site.register(Stock)
admin.site.register(Detail)
admin.site.register(DisplaySr)
admin.site.register(DisplayMo)
admin.site.register(StockCorrelation)
