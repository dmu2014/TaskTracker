from django.contrib import admin
from todo.models import Item, Comment


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'priority', 'due_date', 'assigned_to')
    #readonly_fields = ('id',)
    #list_filter = ('list',)
    ordering = ('priority',)
    search_fields = ('title','note')


#class CommentAdmin(admin.ModelAdmin):
#    list_display = ('author', 'date', 'snippet')


#admin.site.register(List)
admin.site.register(Comment)
admin.site.register(Item, ItemAdmin)
