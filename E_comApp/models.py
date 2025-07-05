from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class customers(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
	name = models.CharField("Name",max_length=(100),null=False,blank=False)
	phonenumber = models.CharField("Phone number",max_length=(11))
	datecreated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class store(models.Model):
	productimage = models.ImageField("Product Image",null=True,blank=True,upload_to = 'upload/',max_length=(200))
	productname = models.CharField("Prduct Name",max_length=(200),null=False,blank=False)
	price = models.DecimalField("Price",max_digits=(5),decimal_places=2)
	datecreated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.productname

class orders(models.Model):
	customers = models.ForeignKey(customers,on_delete=models.SET_NULL, null=True,blank=True)
	orderno = models.CharField("Order No",max_length=(200),null=False,blank=False)
	complete = models.BooleanField("Complete",default=False,null=True,blank=False)
	datecreated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.id)

	@property
	def get_item_cardtotal(self):
		orderitems = self.orderitems_set.all()
		cardtotal = sum([item.get_item_total for item in orderitems])
		return cardtotal

	@property
	def get_item_count(self):
		orderitems = self.orderitems_set.all()
		totqty = sum([item.quantity for item in orderitems])
		return totqty

class orderitems(models.Model):
	orders = models.ForeignKey(orders,on_delete=models.SET_NULL, null=True,blank=True)
	store = models.ForeignKey(store,on_delete=models.SET_NULL,null=True,blank=True)
	quantity = models.IntegerField("Quantity",default=0,null=True,blank=True)
	datecreated = models.DateTimeField(auto_now_add=True)

	@property
	def get_item_total(self):
		subtotal = self.store.price * self.quantity
		return subtotal

class shipsaddress(models.Model):
	customers = models.ForeignKey(customers,on_delete=models.SET_NULL, null=True,blank=True)
	orders = models.ForeignKey(orders,on_delete=models.SET_NULL, null=True,blank=True)
	street = models.CharField("Street",max_length=(100))
	city = models.CharField("City",max_length=(100))
	district = models.CharField("District",max_length=(100))
	state = models.CharField("State",max_length=(100))
	zipcode = models.CharField("Zip Code",max_length=(100))
	datecreated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.city



