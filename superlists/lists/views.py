from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError


# Create your views here.
def home_page(request):
    return render(request, 'home.html')

    items = Item.objects.all()

    return render(request, 'home.html', {'items': items})


def view_list(request, list_Id):
    list_ = List.objects.get(id=list_Id)
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
    except ValidationError:
        list_.delete()
        error = 'Você não pode adicionar um item vazio'
        return render(request, 'home.html', {"error": error})

    return redirect(f'/lists/{list_.id}/')


def add_items(request, list_Id):
    list_ = List.objects.get(id=list_Id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')