from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm 
from .models import Item, BigCategory, SmallCategory
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('user_name',)
 
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['item', 'description', 'big_category'
        , 'small_category', 'price', 'paid_at']

class BigCategoryForm(ModelForm):
    class Meta:
        model = BigCategory
        fields = ['big_category']

class SmallCategoryForm(ModelForm):
    class Meta:
        model = SmallCategory
        fields = ['big_category', 'small_category']

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['item', 'description', 'big_category'
        , 'small_category', 'price', 'paid_at']

class PostCreateForm(forms.ModelForm):
    # 親カテゴリの選択欄がないと絞り込めないので、定義する。
    parent_category = forms.ModelChoiceField(
        label='大カテゴリ',
        queryset=BigCategory.objects,
        required=False
    )

    class Meta:
        model = Item
        fields = '__all__'

    field_order = ('item', 'big_category', 'small_category')