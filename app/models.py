from django.db import models 
from django.contrib.auth import get_user_model
from django.utils import timezone

class BigCategory(models.Model):
    big_category = models.CharField(max_length=20, default='その他', unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    def __str__(self):
        return self.big_category

class SmallCategory(models.Model):
    small_category = models.CharField(max_length=20, default='その他')
    big_category = models.ForeignKey(BigCategory
        , on_delete=models.CASCADE
    )
    class Meta:
        unique_together = ('small_category', 'big_category')
    
    def __str__(self):
        return self.small_category

class Item(models.Model):
    item = models.CharField(max_length=30)     
    description = models.TextField(blank=True)
    small_category = models.ForeignKey(SmallCategory
        , on_delete=models.CASCADE # userを消したら消えるようにしたい,small_categoryだけ消すときは移植作業が必要
    )
    price = models.PositiveIntegerField(default=0)
    paid_at = models.DateField(default=timezone.now)

    def __str__(self):         
        return self.item