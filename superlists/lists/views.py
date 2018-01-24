from django.shortcuts import render, redirect
from lists.models import Item, List


# Create your views here.
def home_page(request):
    return render(request, 'home.html')

    items = Item.objects.all()

    return render(request, 'home.html', {'items': items})


def view_list(request, list_Id):
    list_ = List.objects.get(id=list_Id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'items': items})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
