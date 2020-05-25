<<<<<<< HEAD
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
=======
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm

from bokeh.models import ColumnDataSource, OpenURL, TapTool, CustomJS
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
>>>>>>> 2e536c5c9c8ba1e6aaac3b665c67a644444cf175


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


<<<<<<< HEAD
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
=======
def graph_outgo(request):

    x = [1, 2, 3, 4, 5]
    y = [200, 500, 800, 200, 700]
    point_id = [0, 1, 2, 3, 4]

    for id_ in point_id:
        if "price" in request.session:
            request.session["price"][str(id_)] = y[id_]
        else:
            request.session["price"] = {str(id_): y[id_]}

    price = request.session.get("price", {})
    print(price)

    p = figure(plot_width=400, plot_height=400, tools="tap", title="Click the Dots")

    source = ColumnDataSource(data=dict(x=x, y=y, point_id=point_id,))
    p.line("x", "y", source=source)
    p.circle("x", "y", size=20, source=source)

    # use the "color" column of the CDS to complete the URL
    # e.g. if the glyph at index 10 is selected, then @color
    # will be replaced with source.data['color'][10]
    # url = "http://www.colors.commutercreative.com/@color/"

    url = "http://127.0.0.1:8000/popup_table/@point_id"
    taptool = p.select(type=TapTool)

    taptool.callback = OpenURL(url=url, same_tab=True)

    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files
    script, div = components(p)

    return render(
        request,
        "app/graph_outgo.html",
        {"cdn_js": cdn_js, "cdn_css": cdn_css, "script": script, "div": div},
    )


def popup_table(request, point_id):

    price = request.session["price"]
    print(price)

    return render(request, "app/popup_table.html", {"price": price[str(point_id)]})
>>>>>>> 2e536c5c9c8ba1e6aaac3b665c67a644444cf175
