from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm

from bokeh.models import ColumnDataSource, OpenURL, TapTool, CustomJS
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components


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
