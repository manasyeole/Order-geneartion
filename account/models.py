from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,date
from django.conf import settings

class Order(models.Model):
	created_by = models.CharField(max_length=20)
	isapprovedbydphead = models.BooleanField(default = False)
	isapprovedbysupervisor = models.BooleanField(default = False)
	isapprovedbystoreman = models.BooleanField(default = False)
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "{}".format(self.id)

	def was_published_today(self):
	 	return self.created_on.date() == datetime.date.today()

class MS_list(models.Model):
	Itemname = models.CharField(max_length=50)
	Itemcode = models.IntegerField(primary_key=True)
	Type = models.CharField(max_length=20)
	quantity=models.FloatField()
	price=models.FloatField()

	def __str__(self):
		return "{}".format(self.Itemcode)


class Item(models.Model):
	name = models.CharField(max_length=50)
	item_code = models.IntegerField()
	quantity=models.FloatField()
	rate=models.FloatField()
	amount=models.FloatField()
	Order_id = models.ForeignKey(Order, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Stock(models.Model):
	Departmentname =models.CharField(max_length=50)
	Departmentcode = models.IntegerField(primary_key=True)
	Budjet_alloted_peryear=models.FloatField()
	Budjet_remained=models.FloatField()
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.Departmentname

	def was_published_today(self):
	 	return self.created_on.date() == datetime.date.today()