from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm 
from .models import Item, BigCategory, SmallCategory
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('user_name',)

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
        fields = ['item', 'description', 'small_category', 'price', 'paid_at']

class PostCreateForm(forms.ModelForm):
    big_category = forms.ModelChoiceField(
        label='Big category',
        queryset=None,
        required=False
    )
    def __init__(self, user_ids, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        # queryset に group_ids で filter した クエリーセットをセットする 
        self.fields['big_category'].queryset = BigCategory.objects.filter(user_id=user_ids)
        self.fields['small_category'].queryset = BigCategory.objects.filter(user_id=user_ids)

    class Meta:
        model = Item
        fields = '__all__'

    field_order = ('item', 'description', 'big_category', 'small_category', 'price', 'paid_at')