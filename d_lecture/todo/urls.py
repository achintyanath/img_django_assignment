from django.urls import path
from todo.views import createnewlistheading, delete, deletelist, done, index,detail,create, modify, retrieve

app_name='todo'
urlpatterns = [
    path('',index,name='index'),
    path('<int:list_id>/<int:item_id>/',detail,name='list_detail'),
    path('create/<list_id>',create,name='create'),
    path('delete/<item_id>',delete,name='delete'),
    path('modify/<item_id>',modify,name='modify'),
    path('retrieve/',retrieve,name='retrieve'),
    path('done/<int:list_id>/<int:item_id>/',done,name='done'),
    path('createnewlistheading/',createnewlistheading,name='createnewlistheading'),
    path('deletelist/<list_id>',deletelist,name='deletelist'),
]
