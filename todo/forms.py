from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from todo.models import Item, Comment
from functools import partial
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

Project_Ids = (  
    ('wcc-sw-nfa', 'wcc-sw-nfa'),
    ('wcc-sw-wiced-stack', 'wcc-sw-wiced-stack')    
)


class AddItemForm(ModelForm):
   
    # The picklist showing the users to which a new task can be assigned
    # must find other members of the groups the current list belongs to.

    def save_hasparent(self):
        # If Item is being marked complete, set the completed_date
        #if self.completed:
        #    self.completed_date = datetime.datetime.now()
        super(Item, self.hasparent).save()
    #def __init__(self, *args, **kwargs):
    #    super(AddItemForm, self).__init__(*args, **kwargs)
    #    self.fields['haschildren'] = forms.ChoiceField(choices=get_subcategory_choices() )

    #due_date = forms.DateField(
    #   required=False,
    #    widget=forms.DateTimeInput(attrs={'class': 'due_date_picker'})
    #)

    #title = forms.CharField(
    #    widget=forms.widgets.TextInput(attrs={'size': 35})
    #)

    #note = forms.CharField(widget=forms.Textarea(), required=False)

    #Project_Id = forms.CharField(max_length=50, choices=Project_Ids)
    




    
    class Meta:
        model = Item
        widgets = {
            'due_date': forms.DateInput(attrs={'class':'datepicker'}),
            'completed_date': forms.DateInput(attrs={'class':'datepicker'}),
            'note': SummernoteWidget(),
            #'note': SummernoteInplaceWidget(),
        }

        exclude = ['hasparent','haschildren','parentId']


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        widgets = {
            'text': SummernoteWidget(),
            #'note': SummernoteInplaceWidget(),
        }
        fields = ('text','red_flag')



class EditItemForm(ModelForm):
    # The picklist showing the users to which a new task can be assigned
    # must find other members of the groups the current list belongs to.
    def __init__(self, *args, **kwargs):
        super(EditItemForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(groups__in=[self.instance.list.group])

    class Meta:
        model = Item
        exclude = ('created_date', 'created_by',)


class AddExternalItemForm(ModelForm):
    """Form to allow users who are not part of the GTD system to file a ticket."""

    title = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'size': 35})
    )
    note = forms.CharField(
        widget=forms.widgets.Textarea(),
        help_text='Foo',
    )

    class Meta:
        model = Item
        exclude = ('list', 'created_date', 'due_date', 'created_by', 'assigned_to',)


class SearchForm(forms.Form):
    """Search."""

    q = forms.CharField(
        widget=forms.widgets.TextInput(attrs={'size': 35})
    )
