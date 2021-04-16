from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Segment(models.Model):
    #最大100の文字列フィールド
    segment_name = models.CharField(max_length=100)
    #printするとsegment_nameが返る？adminページの名前になる
    def __str__(self):
        return self.segment_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=100)

    def __str__(self):
        return self.brand_name


class Vehicle(models.Model):
    # Users消えたらCASCADEも消す
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    vehicle_name = models.CharField(max_length=100)
    #整数フィールド
    release_year = models.IntegerField()
    #小数点以下2桁、全桁6の浮動小数点フィールド
    price = models.DecimalField(max_digits=6, decimal_places=2)
    segment = models.ForeignKey(
        Segment,
        on_delete=models.CASCADE
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.vehicle_name
