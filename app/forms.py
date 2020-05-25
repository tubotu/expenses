from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import BigCategory, SmallCategory
from django.shortcuts import get_list_or_404


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("user_name",)


TEST = (
    ("食費1", "食費2"),
    ("食費2", "食費2"),
    ("その他", "その他"),
)


class GraphCategoryForm(forms.Form):

    big_category = get_list_or_404(BigCategory)
    big_category = [(x.big_category, x.big_category,) for x in big_category]
    big_category = tuple(big_category)

    small_category = get_list_or_404(SmallCategory)
    small_category = [(x.small_category, x.small_category,) for x in small_category]
    small_category = tuple(small_category)

    big = forms.ChoiceField(
        label="大カテゴリ", widget=forms.Select, choices=big_category, required=True,
    )

    small = forms.ChoiceField(
        label="小カテゴリ", widget=forms.Select, choices=small_category, required=True,
    )
