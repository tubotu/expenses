from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm 
from .models import Item

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('user_name',)
 
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['item', 'description', 'big_category'
        , 'small_category', 'price', 'paid_at']
