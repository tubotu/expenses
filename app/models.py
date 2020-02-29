from django.db import models 
from django.contrib.auth import get_user_model
from django.utils import timezone

class BigCategory(models.Model):
    big_category = models.CharField(max_length=20, default='その他', unique=True)
    def __str__(self):
        return self.big_category

def set_big_default_category():
    category, _ = BigCategory.objects.get_or_create(big_category='その他')
    return category

class SmallCategory(models.Model):
    small_category = models.CharField(max_length=20, default='その他')
    big_category = models.ForeignKey(BigCategory
        , on_delete=models.CASCADE
    )
    class Meta:
        unique_together = ('small_category', 'big_category')
    
    def __str__(self):
        return self.small_category

def set_small_default_category():
    big_category, _ = BigCategory.objects.get_or_create(big_category='その他')
    small_category, _ = SmallCategory.objects.get_or_create(small_category='その他', big_category=big_category)
    return small_category

class Item(models.Model):
    item = models.CharField(max_length=30)     
    description = models.TextField(blank=True)
    big_category = models.ForeignKey(BigCategory
        , on_delete=models.SET_DEFAULT
        , default=set_big_default_category
    )
    small_category = models.ForeignKey(SmallCategory
        , on_delete=models.SET_DEFAULT
        , default=set_small_default_category
    )
    price = models.PositiveIntegerField(default=0)
    paid_at = models.DateField(default=timezone.now)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    def __str__(self):         
        return self.item
