from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, GraphCategoryForm
from .models import BigCategory, SmallCategory, Item

import numpy
from datetime import datetime
from itertools import groupby
from operator import itemgetter
from django.core import serializers

from django.http import JsonResponse


def index(request):
    return render(request, "app/index.html")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            input_user_name = form.cleaned_data["user_name"]
            input_password = form.cleaned_data["password1"]
            new_user = authenticate(email=input_email, password=input_password)
        if new_user is not None:
            login(request, new_user)
            return redirect("app:index")
    else:
        form = CustomUserCreationForm()
    return render(request, "app/signup.html", {"form": form})


def chartjs(request):

    items = get_list_or_404(Item)

    paid_at = [item.paid_at.date() for item in items]
    price = [item.price for item in items]
    xy = zip(paid_at, price, items)
    xy = sorted(xy, key=itemgetter(0))

    x = []
    y = []
    list_item = []
    for key, group in groupby(xy, itemgetter(0)):

        x.append(key)
        sum_price = 0
        tmp_item = []
        for item in list(group):
            sum_price += item[1]
            tmp_item.append(item[2].id)
        y.append(sum_price)
        list_item.append(tmp_item)

    point_id = list(range(len(x)))

    request.session.clear()

    for id_ in point_id:
        if "item_id" in request.session:
            request.session["item_id"][str(id_)] = list_item[id_]
        else:
            request.session["item_id"] = {str(id_): list_item[id_]}

    x = [tmp.strftime("%m-%d") for tmp in x]

    return render(request, "app/chartjs.html", {"x_axis": x, "y_axis": y})


def ajax_get_itemList(request):

    point_id = request.GET.get("point_id")

    item_id = request.session["item_id"]
    item_id = item_id[str(point_id)]

    items = []
    for id_ in item_id:
        items.append(get_object_or_404(Item, id=id_))

    item_list = [
        {
            "item": item.item,
            "big_category": str(item.big_category),
            "small_category": str(item.small_category),
            "price": item.price,
        }
        for item in items
    ]

    print(item_list)

    return JsonResponse({"itemList": item_list})


def ajax_get_category(request):

    pk = request.GET.get("pk")
    # pkパラメータがない、もしくはpk=空文字列だった場合は全カテゴリを返しておく。
    if not pk:
        category_list = SmallCategory.objects.all()

    # pkがあれば、そのpkでカテゴリを絞り込む
    else:
        category_list = SmallCategory.objects.filter(big_category__pk=pk)

    # [ {'name': 'サッカー', 'pk': '3'}, {...}, {...} ] という感じのリストになる。
    category_list = [
        {"pk": category.pk, "small_category": category.small_category}
        for category in category_list
    ]

    # JSONで返す。
    return JsonResponse({"categoryList": category_list})
