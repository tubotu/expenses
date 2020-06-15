from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Item, BigCategory, SmallCategory
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("user_name",)


class BigCategoryForm(ModelForm):
    class Meta:
        model = BigCategory
        fields = ["big_category"]


class SmallCategoryForm(ModelForm):
    class Meta:
        model = SmallCategory
        fields = ["big_category", "small_category"]


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["item", "description", "small_category", "price", "paid_at"]


class PostCreateForm(forms.ModelForm):
    big_category = forms.ModelChoiceField(
        label="Big category", queryset=None, required=False
    )

    def __init__(self, user_ids, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        # queryset に group_ids で filter した クエリーセットをセットする
        self.fields["big_category"].queryset = BigCategory.objects.filter(
            user_id=user_ids
        )
        self.fields["small_category"].queryset = BigCategory.objects.filter(
            user_id=user_ids
        )

    class Meta:
        model = Item
        fields = "__all__"

    field_order = (
        "item",
        "description",
        "big_category",
        "small_category",
        "price",
        "paid_at",
    )


class GraphForm(forms.Form):
    big_category = forms.ChoiceField(label="big_category", required=False, choices=[])
    small_category = forms.ChoiceField(
        label="small_category", required=False, choices=[]
    )

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop("user_id")
        cat = kwargs.pop("cat")  # 現時点では不要
        super().__init__(*args, **kwargs)  # popより後，selfより前に置かないとエラーになる
        # user_idを元に，big_categoryの表示内容を絞り込み
        tmp = [
            (tmp_cat.pk, tmp_cat.big_category)
            for tmp_cat in BigCategory.objects.filter(user_id=user_id)
        ]
        tmp.insert(0, ("", "すべて"))
        self.fields["big_category"].choices = tmp
        # small_categoryの初期値，要検討
        self.fields["small_category"].choices = [("", "すべて")]
        # self.fields["small_category"].initial = cat formの初期値の設定
