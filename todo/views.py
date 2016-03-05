from django.shortcuts import render_to_response, render
from todo.models import Item, Comment
from todo.forms import AddItemForm, CommentForm, EditItemForm, AddExternalItemForm, SearchForm
from todo import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import redirect
import datetime

# Need for links in email templates
current_site = Site.objects.get_current()

@login_required
def post_list(request):
    title = Item.objects.order_by('id')
    return render(request, 'todo/post_list.html', {'title': title})

def postchild_list(request, parentId):
    post = Item.objects.order_by('id')
    title = Item.objects.filter(parentId__contains = parentId) 
    return render(request, 'todo/postchild_list.html', {'title': title, 'post': post})

def my_tasks(request):
    post = Item.objects.order_by('id')
    
    title = Item.objects.filter(assigned_to = request.user) 
    return render(request, 'todo/postmy_list.html', {'title': title, 'post': post})

def post_detail(request, pk):
    title = Item.objects.order_by('id')
    post = get_object_or_404(Item, pk=pk)
    return render(request, 'todo/post_detail.html', {'post': post, 'title':title})

def childtask_detail(request, cpk, pk):
    childtask = get_object_or_404(ChildTask, pk=cpk)
    post = get_object_or_404(Item, pk=pk)
    return render(request, 'todo/childtask_detail.html', {'post': post, 'childtask':childtask})

def post_new(request):
    if request.method == "POST":
        form = AddItemForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post = form.save()
            #post.pk = str(int(post.pk) + 1)
            post.created_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = AddItemForm()
        #post = form.save(commit=False)
        #post = form.save()
        #post.pk = str(int(post.pk) + 1)
    return render(request, 'todo/post_edit.html', {'form': form})

def postchild_new(request, pk):
    post = get_object_or_404(Item, pk=pk)
    post.haschildren = True
    post.save()
    if request.method == "POST":
        form = AddItemForm(request.POST)
        
        if form.is_valid():
            
            
            
            childpost = form.save(commit=False)
            #post = form.save()
            #post.pk = str(int(post.pk) + 1)
            childpost.hasparent = True
            
            childpost.parentId = pk
            childpost.created_date = timezone.now()
            childpost.save()
            
            
            return redirect('post_detail', pk=childpost.pk)
    else:
        form = AddItemForm()
        
        #post = form.save(commit=False)
        #post = form.save()
        #post.pk = str(int(post.pk) + 1)
    return render(request, 'todo/post_edit.html', {'form': form})

def post_edit(request,pk):
    post = get_object_or_404(Item, pk=pk)
    #projectID = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = AddItemForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            #item.author = request.user
            post.created_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = AddItemForm(instance=post)
    return render(request, 'todo/post_edit.html', {'form': form})


def post_remove(request, pk):
    post = get_object_or_404(Item, pk=pk)
    post.delete()
    return redirect('todo.views.post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Item, pk=pk)
    #del_comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.item = post
            comment.author = str(request.user)
            #post.comments = comment
            comment.save()
            #post.save()
            return redirect('todo.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'todo/add_comment_to_post.html', {'form': form})

def comment_edit(request,pk):
    #post = get_object_or_404(Item, pk=pk)
    del_comment = get_object_or_404(Comment, pk=pk)
    #post_pk = del_comment.item.pk
    #del_comment.delete()
    if request.method == "POST":
        form = CommentForm(request.POST, instance=del_comment)
        if form.is_valid():
            comment = form.save(commit=False)
            #comment.item = post
            #post.comments = comment
            comment.author = str(request.user)
            comment.date = datetime.datetime.now()
            post_pk = comment.item.pk
            comment.save()
            
            #post.save()
            return redirect('todo.views.post_detail', post_pk)
    else:
        form = CommentForm(instance=del_comment)
    #del_comment.delete()
    return render(request, 'todo/add_comment_to_post.html', {'form': form})

def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.item.pk
    comment.delete()
    return redirect('todo.views.post_detail', pk=post_pk)

def childtask_remove(request, pk):
    childtask = get_object_or_404(ChildTask, pk=pk)
    post_pk = childtask.childtask.pk
    childtask.delete()
    return redirect('todo.views.post_detail', pk=post_pk)

def check_user_allowed(user):
    """
    test for user_passes_test decorator
    """
    if settings.STAFF_ONLY:
        return user.is_authenticated() and user.is_staff
    else:
        return user.is_authenticated()


@user_passes_test(check_user_allowed)
def view_task(request, task_id):
    """
    View task details. Allow task details to be edited.
    """
    task = get_object_or_404(Item, pk=task_id)
    comment_list = Comment.objects.filter(task=task_id)

    # Before doing anything, make sure the accessing user has permission to view this item.
    # Determine the group this task belongs to, and check whether current user is a member of that group.
    # Admins can edit all tasks.

    if task.list.group in request.user.groups.all() or request.user.is_staff:

        auth_ok = 1
        if request.POST:
            form = EditItemForm(request.POST, instance=task)

            if form.is_valid():
                form.save()

                # Also save submitted comment, if non-empty
                if request.POST['comment-body']:
                    c = Comment(
                        author=request.user,
                        task=task,
                        body=request.POST['comment-body'],
                    )
                    c.save()

                    # And email comment to all people who have participated in this thread.
                    email_subject = render_to_string("todo/email/assigned_subject.txt", {'task': task})
                    email_body = render_to_string("todo/email/newcomment_body.txt",
                                                  {'task': task, 'body': request.POST['comment-body'],
                                                   'site': current_site, 'user': request.user})

                    # Get list of all thread participants - task creator plus everyone who has commented on it.
                    recip_list = []
                    recip_list.append(task.created_by.email)
                    commenters = Comment.objects.filter(task=task)
                    for c in commenters:
                        recip_list.append(c.author.email)
                    # Eliminate duplicate emails with the Python set() function
                    recip_list = set(recip_list)

                    # Send message
                    try:
                        send_mail(email_subject, email_body, task.created_by.email, recip_list, fail_silently=False)
                        messages.success(request, "Comment sent to thread participants.")

                    except:
                        messages.error(request, "Comment saved but mail not sent. Contact your administrator.")

                messages.success(request, "The task has been edited.")

                return HttpResponseRedirect(reverse('todo-incomplete_tasks', args=[task.list.id, task.list.slug]))
        else:
            form = EditItemForm(instance=task)
            if task.due_date:
                thedate = task.due_date
            else:
                thedate = datetime.datetime.now()
    else:
        messages.info(request, "You do not have permission to view/edit this task.")

    return render_to_response('todo/view_task.html', locals(), context_instance=RequestContext(request))


@csrf_exempt
@user_passes_test(check_user_allowed)
def reorder_tasks(request):
    """
    Handle task re-ordering (priorities) from JQuery drag/drop in view_list.html
    """
    newtasklist = request.POST.getlist('tasktable[]')
    # First item in received list is always empty - remove it
    del newtasklist[0]

    # Items arrive in order, so all we need to do is increment up from one, saving
    # "i" as the new priority for the current object.
    i = 1
    for t in newtasklist:
        newitem = Item.objects.get(pk=t)
        newitem.priority = i
        newitem.save()
        i = i + 1

    # All views must return an httpresponse of some kind ... without this we get
    # error 500s in the log even though things look peachy in the browser.
    return HttpResponse(status=201)


@login_required
def external_add(request):
    """
    Allow users who don't have access to the rest of the ticket system to file a ticket in a specific list.
    This is useful if, for example, a core web team are in a group that can file todos for each other,
    but you also want students to be able to post trouble tickets to a list just for the sysadmin. This
    way we don't have to put all users into a group that gives them access to the whole ticket system.
    """
    if request.POST:
        form = AddExternalItemForm(request.POST)

        if form.is_valid():
            # Don't commit the save until we've added in the fields we need to set
            item = form.save(commit=False)
            item.list_id = settings.DEFAULT_LIST_ID
            item.created_by = request.user
            item.assigned_to = User.objects.get(username=settings.DEFAULT_ASSIGNEE)
            item.save()

            # Send email
            email_subject = render_to_string("todo/email/assigned_subject.txt", {'task': item.title})
            email_body = render_to_string("todo/email/assigned_body.txt", {'task': item, 'site': current_site, })
            try:
                send_mail(email_subject, email_body, item.created_by.email, [item.assigned_to.email],
                          fail_silently=False)
            except:
                messages.error(request, "Task saved but mail not sent. Contact your administrator.")

            messages.success(request, "Your trouble ticket has been submitted. We'll get back to you soon.")

            return HttpResponseRedirect(reverse(settings.PUBLIC_SUBMIT_REDIRECT))
    else:
        form = AddExternalItemForm()

    return render_to_response('todo/add_external_task.html', locals(), context_instance=RequestContext(request))


@user_passes_test(check_user_allowed)
def search_post(request):
    """
    Redirect POST'd search param to query GET string
    """
    if request.POST:
        q = request.POST.get('q')
        url = reverse('todo-search') + "?q=" + q
        return HttpResponseRedirect(url)


@user_passes_test(check_user_allowed)
def search(request):
    """
    Search for tasks
    """
    if request.GET:

        query_string = ''
        found_items = None
        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']

            found_items = Item.objects.filter(
                Q(title__icontains=query_string) |
                Q(note__icontains=query_string)
            )
        else:

            # What if they selected the "completed" toggle but didn't type in a query string?
            # In that case we still need found_items in a queryset so it can be "excluded" below.
            found_items = Item.objects.all()

        if 'inc_complete' in request.GET:
            found_items = found_items.exclude(completed=True)

    else:
        query_string = None
        found_items = None

    return render_to_response('todo/search_results.html',
                              {'query_string': query_string, 'found_items': found_items},
                              context_instance=RequestContext(request))
