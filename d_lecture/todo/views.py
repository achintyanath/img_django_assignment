"""
    This module controls the actions that can be performed on app.

    Methods:
    index, detail, create, delete, modify, retrieve, done, createnewlistheading, deletelist

"""


from django.http.response import Http404
from django.shortcuts import redirect, render
#from django.http import HttpResponse
#from django.template import loader
from todo.models import TodoList,TodoItem
from django.core.exceptions import BadRequest


def index(request):
    """
    This function displays the first page of app.
    This passes all the TodoList and TodoItem Object to index.html

    Parameters:
        request: The request object

    Return:
        It renders the index.html page

    """

    list_todo= TodoList.objects.all()
    items =TodoItem.objects.all()

    context={
        'todolists': list_todo,
        'todoitems': items
    }

    return render(request, 'todo/index.html', context)



def detail(request, list_id,item_id):

    """
    This function displays the details of a particular task.

    Parameters:
        request: The request object.
        list_id: The id of the list to which the task belongs
        item_id: The id of task object.

    Return:
        It renders the details.html page

    """
    try:
        todolist=TodoList.objects.get(id=list_id)
        todoitem = TodoItem.objects.get(id=item_id)
    except:
        raise Http404 ("The list doesn't exist")


    todolist = TodoList.objects.get(id=list_id)
    items_list = TodoItem.objects.filter(id=item_id)
    context = {
        'todolist': todolist,
        'items_list': items_list,
        'todoitem':todoitem
    }
    return render(request, 'todo/detail.html', context)


def create(request,list_id):
    """
    This function creates a new task under the given list.

    Parameters:
        request: The request object.
        list_id: The id of the list to which the task is to be added.

    Return:
        When request method is get, it renders createlist.html
        When request method is post, it creates list and then redirects to homepage.

    """

    try:
        todolist=TodoList.objects.get(id=list_id)
    except:
        raise Http404 ("The list doesn't exist")
  
    context={
        'list_id' : list_id
    }


    if request.method == 'GET':
        return render(request, 'todo/createlist.html',context)


    try:    
        name = request.POST["name"]
        date = request.POST["duetime"]
    except:
        raise BadRequest('Invalid request.')

    if(name==""):
        return render(request,  "todo/emptylist.html/")

    try:
        item = TodoItem.objects.get(title=name)
        return render(request,  "todo/alreadyexist.html/")
    except:
        TodoItem.objects.create(title=name,due_date=date,todo_list=TodoList.objects.get(id=list_id))
        return redirect('/todo/')


def delete(request,item_id):

    """
    This function deletes a task.

    Parameters:
        request: The request object.
        item_id: The id of the task which is to be deleted.

    Return:
        It redirects to homepage.

    """

    try:
       todoitem = TodoItem.objects.get(id=item_id) 
    except:
        raise Http404 ("The list doesn't exist")

    item = TodoItem.objects.get(id=item_id)
    print(item)
    item.delete()

    return redirect('/todo/',)


def modify(request,item_id):
    """
    This function modifies a task.

    Parameters:
        request: The request object.
        item_id: The id of the task which is to be modified.

    Return:
        When request method is get, it renders modify.html
        When request method is post, it creates list and then redirects to homepage.

    """

    try:
       todoitem = TodoItem.objects.get(id=item_id) 
    except:
        raise Http404 ("The list doesn't exist")

    item = TodoItem.objects.get(id=item_id)
    context={
        'item_id' : item_id,
        'item':item
    }

    if request.method == 'GET':
        return render(request, 'todo/modify.html',context)


    try:    
        name = request.POST["name"]
        date = request.POST["duetime"]
    except:
        raise BadRequest('Invalid request.')

    name = request.POST["name"]
    date = request.POST["duetime"]

    if(name==""):
        return render(request,  "todo/emptylist.html/")
    
        
    try:    
        item1 = TodoItem.objects.get(title=name)
        return render(request,  "todo/alreadyexist.html/")
    except:
        item=TodoItem.objects.filter(id=item_id).update(title=name,due_date=date)
        return redirect('/todo/')


def retrieve(request):
    """
    This function finds a particular task.

    Parameters:
        request: The request object.

    Return:
        When request method is get, it renders retrieve.html
        When request method is post, it renders the details.html of that task.

    """
    if request.method == 'GET':
        return render(request, 'todo/retrieve.html')


    try:    
        name = request.POST["name"]
    except:
        raise BadRequest('Invalid request.')


    name = request.POST["name"]
    try:
        item=TodoItem.objects.get(title=name)
    except:
        return render(request,  "todo/retrievenotfound.html/")

    list_name = item.todo_list
    list_id =list_name.id
    item_id = item.id
    return redirect(f"/todo/{list_id}/{item_id}/")


def done(request,list_id,item_id):
    """
    This function marks a task as complete or incomplete.

    Parameters:
        request: The request object.
        list_id: The id of the list to which the task belongs
        item_id: The id of task object whose done status is to be changed.

    Return:
        It redirects to the details.html of that task.

    """

    try:
        todolist=TodoList.objects.get(id=list_id)
        todoitem = TodoItem.objects.get(id=item_id)
    except:
        raise Http404 ("The list doesn't exist")

    item = TodoItem.objects.get(id=item_id)
    checkedi = item.checked
    TodoItem.objects.filter(id=item_id).update(checked=not checkedi)

    return redirect(f"/todo/{list_id}/{item_id}/")


def createnewlistheading(request):

    """
    This function creates a new list.

    Parameters:
        request: The request object.

    Return:
        It redirects to the homepage.

    """

    if request.method == "GET":
        return render(request, 'todo/createnewlistheading.html')

    try:    
        name = request.POST["name"]
    except:
        raise BadRequest('Invalid request.')

    name = request.POST["name"]
    
    if(name==""):
        return render(request,  "todo/emptylist.html/")

        
    try:
        item1 = TodoList.objects.get(list_name=name)
        return render(request,  "todo/alreadyexist.html/")
    except:
        TodoList.objects.create(list_name=name)
        return redirect('/todo/')

def deletelist(request,list_id):

    """
    This function deletes a new list.

    Parameters:
        request: The request object.
        list_id: The id of the list which has to be deleted.

    Return:
        It redirects to the homepage.

    """

    try:
        todolist=TodoList.objects.get(id=list_id)
    except:
        raise Http404 ("The list doesn't exist")

    item = TodoList.objects.get(id=list_id)
    item.delete()
    return redirect('/todo/')
