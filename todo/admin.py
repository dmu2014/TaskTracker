from django.contrib import admin
from todo.models import Item, Comment

#from todo.models import Item, Comment, Project, SubProject



class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'priority', 'due_date', 'assigned_to')
    #readonly_fields = ('id',)
    #list_filter = ('list',)
    ordering = ('priority',)
    search_fields = ('title','note')



#class ProjectsAdmin(admin.ModelAdmin):
    #list_display = ('name',)
    #readonly_fields = ('id',)
    #list_filter = ('list',)
    
#class SubProjectsAdmin(admin.ModelAdmin):
    #list_display = ('name',)
    #readonly_fields = ('id',)
    #list_filter = ('list',)
    



#class CommentAdmin(admin.ModelAdmin):
#    list_display = ('author', 'date', 'snippet')


#admin.site.register(List)

#admin.site.register(Comment, CommentAdmin)
#admin.site.register(Project, ProjectsAdmin)
#admin.site.register(SubProject, SubProjectsAdmin)

admin.site.register(Comment)
admin.site.register(Item, ItemAdmin)
