from __future__ import unicode_literals
import datetime

from django.db import models
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from smart_selects.db_fields import ChainedForeignKey 

STATES = (  
    ('New', 'New'),
    ('In Progress', 'In Progress'),
    ('Complete', 'Complete'),
)

PRIORITIES = (  
    ('Low', 'Low'),
    ('Normal', 'Normal'),
    ('High', 'High'),
)

Project_Ids = (  
    ('wcc-sw-nfa', 'wcc-sw-nfa'),
    ('wcc-sw-wiced-stack', 'wcc-sw-wiced-stack')    
)

Subcategory_Ids = (  
    ('NFA11', 'NFA11'),
    ('NFA20', 'NFA20'),
    ('NFCA 3.0','NFCA 3.0'),
    ('BTEWICED 2.0','BTEWICED 2.0')
)



    

@python_2_unicode_compatible
class Item(models.Model):
    
    #task_Id = models.AutoField(null=False, default=("1"))
    #id = models.AutoField(primary_key=True,unique=True, default='99' )
    Project_Id = models.CharField(max_length=140, choices = Project_Ids, default="Add Project ID here")
    subcategory_Id = models.CharField(max_length=140, choices=Subcategory_Ids, default="Add Sub Project ID here")
    #task_Id = models.IntegerField(default = id.value, null=False)
    assigned_to = models.CharField(max_length=50, null=False)
    title = models.CharField(max_length=140,null=False, blank=True, default=(""))
    #list = models.ForeignKey(List)
    created_date = models.DateField(auto_now=True)
    assigned_to = models.ForeignKey(User, related_name='todo_assigned_to')
    created_by = models.ForeignKey(User, related_name='todo_created_by')
    #created_by = models.ForeignKey(User, default='admin')
    #State = models.CharField(max_length=140, default=("In Progress"), null=True)
    State = models.CharField(max_length=16, choices=STATES, default=("New"))
    due_date = models.DateField(blank=True, null=True )
    #completed = models.NullBooleanField(default=None, null=True)
    completed_date = models.DateField(blank=True, null=True)
    note = models.TextField(max_length=400, null=True)
    #Status = models.CharField(max_length=140, null=True)
    #time_allocated = models.CharField(max_length=140, null=True)
    priority = models.CharField(max_length=6, choices=PRIORITIES, default=("Normal"))
    hasparent = models.NullBooleanField()
    haschildren = models.NullBooleanField()
    parentId = models.IntegerField(default=0)
    
    
    # Model method: Has due date for an instance of this object passed?
    def overdue_status(self):
        "Returns whether the item's due date has passed or not."
        if self.due_date and datetime.date.today() > self.due_date:
            return 1

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.id
    
    def get_absolute_url(self):
        return reverse('todo-task_detail', kwargs={'task_id': self.id, })

    # Auto-set the item creation / completed date
    def save(self):
        # If Item is being marked complete, set the completed_date
        #if self.completed:
        #    self.completed_date = datetime.datetime.now()
        super(Item, self).save()

    class Meta:
        ordering = ["priority"]


        

@python_2_unicode_compatible
class Comment(models.Model):
    """
    Not using Django's built-in comments because we want to be able to save
    a comment and change task details at the same time. Rolling our own since it's easy.
    """
    item = models.ForeignKey('todo.Item', related_name='comments',default='99')
    text = models.TextField(null=False, default = ("Add updates here"))
    author = models.CharField(max_length=40, null=False, default = ("Add Author"))
    date = models.DateTimeField(default=datetime.datetime.now)
    red_flag = models.BooleanField(default=None)
    

    def snippet(self):
        # Define here rather than in __str__ so we can use it in the admin list_display
        return "%s - %s...".format(author=self.author, snippet=self.text[:35])
        #return "Hello"

    def __str__(self):
        #return unicode(self.snippet)
        return unicode(self.text)

    def save(self):
        # If Item is being marked complete, set the completed_date
        super(Comment, self).save()

    class Meta:
        ordering = ('-date',)




    
