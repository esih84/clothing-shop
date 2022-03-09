from django.contrib import admin
from .models import post , category
# Register your models here.

class categoryadmin(admin.ModelAdmin):
    list_display = ('title','slug', 'status', 'position')
    list_filter = (['status'])  # serch bar asase che bashad
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(category,categoryadmin)

class adminpost(admin.ModelAdmin):
    list_display = ('name','slug', 'publish','category_to_str','dir')
    search_fields = ('dir', 'name')
    list_filter = ('publish', 'status')  # serch bar asase che bashad
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['status', 'publish']
    def category_to_str(self,obj):
        return ",".join([category.title for category in obj.category.all()])
admin.site.register(post,adminpost)