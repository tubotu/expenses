from django.db import models 
from django.contrib.auth import get_user_model

class BigCategory(models.Model):
    big_category = models.CharField(max_length=20, default='その他')
    def __str__(self):
        return self.big_category

class SmallCategory(models.Model):
    small_category = models.CharField(max_length=20, default='その他')
    big_category = models.ForeignKey(BigCategory
        , on_delete=models.SET_DEFAULT
        , default="""BigCategory.objects.get_or_create(big_category='その他')[0]""" 'その他')
    def __str__(self):
        return self.small_category

class Item(models.Model):
    item = models.CharField(max_length=30)     
    description = models.TextField(blank=True)
    big_category = models.ForeignKey(BigCategory, on_delete=models.SET_DEFAULT, default=BigCategory.objects.get_or_create(big_category='その他')[0])
    """
    small_category = models.ForeignKey(
        SmallCategory
        , on_delete=models.SET_DEFAULT
        , default=SmallCategory.objects.get_or_create(small_category='その他', big_category=big_category.big_category)[0])
    """
    price = models.PositiveIntegerField(default=0)
    paid_at = models.DateTimeField()
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

 
    def __str__(self):         
        return self.item