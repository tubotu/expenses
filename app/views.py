from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import (
    CustomUserCreationForm,
    BigCategoryForm,
    SmallCategoryForm,
    PostCreateForm,
    GraphForm,
)
from django.contrib import messages
from django.http import JsonResponse
from django.views import generic
from .models import Item, BigCategory, SmallCategory

from itertools import groupby
from operator import itemgetter


def index(request):
    return render(request, "app/index.html")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            input_user_name = form.cleaned_data["user_name"]
            input_password = form.cleaned_data["password1"]
            new_user = authenticate(email=input_user_name, password=input_password)
            if new_user is not None:
                login(request, new_user)
                return redirect("app:index")
    else:
        form = CustomUserCreationForm()
    return render(request, "app/signup.html", {"form": form})


@login_required
def big_category_new(request):
    if request.method == "POST":
        form = BigCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, "投稿が完了しました！")
        return redirect("app:index")
    else:
        form = BigCategoryForm()
    return render(request, "app/big_category_new.html", {"form": form})


@login_required
def small_category_new(request):
    if request.method == "POST":
        form = SmallCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            messages.success(request, "投稿が完了しました！")
        return redirect("app:index")
    else:
        form = SmallCategoryForm()
    return render(request, "app/small_category_new.html", {"form": form})


class PostCreate(generic.CreateView):
    model = Item
    form_class = PostCreateForm
    success_url = "/"
    template_name = "app/item_new.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(PostCreate, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(PostCreate, self).get_form_kwargs()
        kwargs["user_ids"] = self.request.user.id
        return kwargs


def ajax_get_category(request):
    pk = request.GET.get("pk")
    # pkパラメータがない、もしくはpk=空文字列だった場合は全カテゴリを返しておく。
    if not pk:
        small_category_list = SmallCategory.objects.all()

    # pkがあれば、そのpkでカテゴリを絞り込む
    else:
        small_category_list = SmallCategory.objects.filter(big_category__pk=pk)

    # json形式のリスト
    small_category_list = [
        {"pk": small_category.pk, "name": small_category.small_category}
        for small_category in small_category_list
    ]

    # JSONで返す。
    return JsonResponse({"smallCategoryList": small_category_list})


class Graph(generic.ListView):
    model = Item
    success_url = "/"
    template_name = "app/graph.html"
    """
    def post(self, request, *args, **kwargs):
        # 検索ボタンを押した後の処理
        form_value = [
            self.request.POST.get("big_category", None),
            self.request.POST.get("small_category", None),
        ]
        request.session["form_value"] = form_value

        return self.get(request, *args, **kwargs)
    
    def get_queryset(self):
        # itemをすべて表示
        user_id = self.request.user.id

        return Item.objects.filter(small_category__big_category__user_id=user_id)
    """

    def get_context_data(self, **kwargs):
        # formとグラフの描画に必要な情報をページに送信する
        """
        # postの処理（小カテゴリだけを選択して送信されると困るなぁ）
        if "form_value" in self.request.session:
            form_value = self.request.session["form_value"]
            big_category = form_value[0]
            small_category = form_value[1]
        else:
            big_category = ""
            small_category = ""

        # postに合わせてアイテムを削減，カテゴリの表示名を取得（すべてのカテゴリ対応を改善したい）
        # contextに選択したカテゴリ名を含めるかどうかは要検討
        if big_category:
            items = items.filter(small_category__big_category=big_category)
            tmp_query = BigCategory.objects.filter(pk=big_category)
            context["big_category"] = {
                "name": tmp_query[0].big_category,
                "pk": tmp_query[0].pk,
            }
            # context["form"].fields["big_category"].initial = big_category
        else:
            context["big_category"] = {
                "name": "すべて",
                "pk": "",
            }
        if small_category:
            items = items.filter(small_category=small_category)
            tmp_query = SmallCategory.objects.filter(pk=small_category)
            context["small_category"] = {
                "name": tmp_query[0].small_category,
                "pk": tmp_query[0].pk,
            }
            # context["form"].fields["small_category"].initial = small_category
        else:
            context["small_category"] = {
                "name": "すべて",
                "pk": "",
            }
        """
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        context["form"] = GraphForm(user_id=self.request.user.id)

        items = Item.objects.filter(small_category__big_category__user_id=user_id)
        # グラフの描画に必要な情報の計算
        paid_at = [item.paid_at for item in items]
        price = [item.price for item in items]
        xy = zip(paid_at, price, items)
        xy = sorted(xy, key=itemgetter(0))
        # x軸, y軸
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
        x = [tmp.strftime("%m-%d") for tmp in x]  # datetimeから文字列へと変換
        # セッションにitem_idを記録
        point_id = list(range(len(x)))
        self.request.session["item_id"] = {}
        for id_ in point_id:
            if "item_id" in self.request.session:
                self.request.session["item_id"][str(id_)] = list_item[id_]
            else:
                self.request.session["item_id"] = {str(id_): list_item[id_]}
        # 絞り込んだアイテムから，横軸と縦軸を計算
        month_total = []
        for month, total in zip(x, y):
            month_total.append({"month": month, "total": total})
        context["month_total"] = month_total

        return context


def ajax_get_graph(request):
    # 変更されたカテゴリに対して絞込み
    small_category_selected = request.GET.get("small_category_selected")
    big_category_selected = request.GET.get("big_category_selected")
    user_id = request.user.id
    print(small_category_selected)
    print(big_category_selected)
    items = Item.objects.filter(small_category__big_category__user_id=user_id)
    print(items)
    if big_category_selected:
        items = items.filter(small_category__big_category=big_category_selected)
    print(items)
    if small_category_selected:
        items = items.filter(small_category=small_category_selected)
    print(items)
    print("!!!")
    # グラフの描画に必要な情報の計算
    paid_at = [item.paid_at for item in items]
    price = [item.price for item in items]
    xy = zip(paid_at, price, items)
    xy = sorted(xy, key=itemgetter(0))
    # x軸, y軸
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
    x = [tmp.strftime("%m-%d") for tmp in x]  # datetimeから文字列へと変換
    # セッションにitem_idを記録
    point_id = list(range(len(x)))
    print(request.session["item_id"])
    request.session["item_id"] = {}
    for id_ in point_id:
        if "item_id" in request.session:
            request.session["item_id"][str(id_)] = list_item[id_]
        else:
            request.session["item_id"] = {str(id_): list_item[id_]}
    # 絞り込んだアイテムから，横軸と縦軸を計算
    month_total = []
    for month, total in zip(x, y):
        month_total.append({"month": month, "total": total})

    return JsonResponse({"month_total": month_total})


def ajax_get_item(request):
    # グラフのクリックした点に合わせて関連するアイテムを表示
    point_id = request.GET.get("point_id")
    item_id = request.session["item_id"]
    item_id = item_id[str(point_id)]

    items = []
    for id_ in item_id:
        items.append(get_object_or_404(Item, id=id_))

    item_list = [
        {
            "item": item.item,
            "big_category": BigCategory.objects.filter(smallcategory__item__pk=item.id)[
                0
            ].big_category,
            "small_category": str(item.small_category),
            "price": item.price,
        }
        for item in items
    ]

    return JsonResponse({"itemList": item_list})
