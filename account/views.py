from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from simple_search import search_filter
from .models import Order
from .models import Item
from .models import MS_list
from .models import Stock



#Function for Login in 
def getin (request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username,password=password)
		obj = Order.objects.all()
		context = {
			"object_list": obj
		}

		if user is not None:
			login(request, user)
			return redirect(reverse("account:index"))
		else:
			messages.info(request,'Invalid Credentials')
			return redirect("account:getin")
	else:
		return render(request,'getin.html')

# Function for Registration
def register (request):
	if request.method == 'POST':
		username =request.POST.get('username')
		password =request.POST.get('password1')
		password2 =request.POST.get('password2')

		if password == password2:
			if User.objects.filter(username=username).exists():
				messages.info(request,'Username Taken')
				return redirect('account:register')
			else:
				user = User.objects.create_user(username=username, password=password )
				user.save()
				return redirect('account:getin')
		else:
			messages.info(request,'Password Not Matching...')
			return redirect('account:register')
		return redirect('/')
	else:
		return render(request,'register.html')

# Function for Logout
def getout(request):
	logout(request)
	return redirect("/")


# Function for main Index Page
# Html Template:index.html
def index(request):
	if(request.user.is_superuser):
		Orders=Order.objects.all().filter(isapprovedbysupervisor=True,isapprovedbydphead=False)
		return render(request,"index.html",{"Orders":Orders})

	elif(request.user.is_staff):
		Orders=Order.objects.all().filter(isapprovedbydphead=True,isapprovedbystoreman=False)
		return render(request,"index.html",{"Orders":Orders})

	elif( request.user.is_authenticated):
		if request.method == 'POST':
			# Item_name=request.POST.get('Item_Name')
			quantity = request.POST.get('quantity')
			# rate = request.POST.get('rate')
			item_code=request.POST.get('Item_Code')
			item_id=MS_list.objects.get(Itemcode=item_code)
			if item_id.quantity < float(quantity):
				messages.error(request,"Quantity available:{}".format(item_id.quantity))
				return redirect(reverse("account:index"))
			ids = request.POST.get('Order_id')
			ids=int(ids)
			order_id=Order.objects.get(pk=ids)
			Item_name=item_id.Itemname
			rate=item_id.price
			amount =float(rate)*float(quantity)
			tim = Item(name=Item_name,item_code=item_code,quantity=quantity,rate=rate,amount=amount,Order_id=order_id)
			tim.save()
			return redirect(reverse("account:index"))
		else:
			obj = Item.objects.all().order_by("Order_id")
			orders=Order.objects.all()
			name_item=MS_list.objects.all()
			Orders=Order.objects.all().filter(isapprovedbystoreman=True)
			Allorders=Order.objects.all().filter(isapprovedbysupervisor=False)
			context = {
			     "object_list": obj,
			     "orders":orders,
			     "Orders":Orders,
			     "name_item":name_item,
			     "Allorders":Allorders,
			    }
			return render(request,'index.html',context)
		return render(request,'index.html')
	return render(request,'index.html')

# Function for Display of list created by supervisor In Order creation section [Index Page]
# Html Template:supervisorlist.html
def get_listsupervisor(request,id):
    items=Item.objects.filter(Order_id=id )
    total=0
    for item in items:
    	total+=item.amount
    budjets=Stock.objects.filter(Departmentcode=1001)
    Total_Budjet=0
    Remaining_Budjet=0
    Remained_Budjet=0
    for budjet in budjets:
    	Total_Budjet=budjet.Budjet_alloted_peryear
    	Remaining_Budjet=budjet.Budjet_remained
    	Remained_Budjet=((Remaining_Budjet)-(total))
    orders=Order.objects.all().filter(isapprovedbysupervisor=False)
    if request.method == 'POST':
    	ids = request.POST.get('Order_id')
    	isapprovedbysupervisor=request.POST.get('isapprovedbysupervisor')
    	Order.objects.filter(pk=ids).update(isapprovedbysupervisor=isapprovedbysupervisor)
    	# Stock.objects.filter(pk=1001).update(Budjet_remained=Remained_Budjet)
    	return redirect(reverse("account:index"))
    context = {
    	"orders":orders,
    	"items":items,
    	"total":total,
    	"RemainingBudjet":Remaining_Budjet,
    	"Total_Budjet":Total_Budjet,
    	"RemainedBudjet":Remained_Budjet,
    	}
    return render(request,"supervisorlist.html",context)

# Delete Function for Delete in get-listsupervisor
def delete_in_get_listsupervisor(request,id,order_id):
	item= Item.objects.get(pk=id)
	item.delete()
	return redirect(reverse('account:get-listsupervisor',kwargs={"id":order_id}))

# Function for Updating masterlist 
# Html Template:Update_MSlist.html
def Update_MSlist(request):
	if request.method == 'POST':
		Itemcode=request.POST.get('Itemcode')
		Itemname=request.POST.get('Itemname')
		Type=request.POST.get('Type')
		new_item = MS_list(Itemcode=Itemcode,Itemname=Itemname,Type=Type,quantity=0,price=0)
		new_item.save()
		return redirect(reverse("account:Update_MSlist"))
	else:
		Ms_list = MS_list.objects.all()
		return render(request,"Update_MSlist.html",{"Ms_list":Ms_list})

# Delete Function for Delete in Update_MSlist
# Html Template:edit_Update_MSlist.html
def edit_Update_MSlist(request,id):
	if request.method == 'POST':
		item= MS_list.objects.get(pk=id)
		quantity=item.quantity
		price=item.price
		Itemcode=request.POST.get('Itemcode')
		Itemname=request.POST.get('Itemname')
		Type=request.POST.get('Type')
		MS_list.objects.filter(pk=id).update(Itemcode=Itemcode,Itemname=Itemname,Type=Type,quantity=quantity,price=price)
		return redirect(reverse("account:Update_MSlist"))
	else:
		item= MS_list.objects.get(pk=id)
		return render(request,"edit_Update_MSlist.html",{"item":item})

# Delete Function for Delete in Update_MSlist
def delete_Update_MSlist(request,id):
	item= MS_list.objects.get(pk=id)
	item.delete()
	return redirect(reverse('account:Update_MSlist'))

# Function for Adding Departmnet
# Html Template:Add_Department.html
def Add_Department(request):
	if request.method == 'POST':
		Departmentname=request.POST.get('Departmentname')
		Departmentcode=request.POST.get('Departmentcode')
		Budjet_alloted_peryear=request.POST.get('Budjet_alloted_peryear')
		new_item = Stock(Departmentname=Departmentname,Departmentcode=Departmentcode,Budjet_alloted_peryear=Budjet_alloted_peryear,Budjet_remained=Budjet_alloted_peryear)
		new_item.save()
		return redirect(reverse("account:Add_Department"))
	else:
		Department_data = Stock.objects.all()
		return render(request,"Add_Department.html",{"Department_data":Department_data})


# Delete Function for Delete in Add_Department
# Html Template:edit_Add_Department.html
def edit_Add_Department(request,id):
	if request.method == 'POST':
		item= Stock.objects.get(pk=id)
		Budjet_remained=item.Budjet_remained
		Departmentname=request.POST.get('Departmentname')
		Departmentcode=request.POST.get('Departmentcode')
		Budjet_alloted_peryear=request.POST.get('Budjet_alloted_peryear')
		Stock.objects.filter(pk=id).update(Departmentname=Departmentname,Departmentcode=Departmentcode,Budjet_alloted_peryear=Budjet_alloted_peryear,Budjet_remained=Budjet_remained)
		return redirect(reverse("account:Add_Department"))
	else:
		item= Stock.objects.get(pk=id)
		return render(request,"edit_Add_Department.html",{"item":item})

# Delete Function for Delete in Add_Department
def delete_Add_Department(request,id):
	item= Stock.objects.get(pk=id)
	item.delete()
	return redirect(reverse('account:Add_Department'))

# Function for Creating Ordering
# Html Template:Create_Order.html
def Create_Order(request):
	if request.method == 'POST':
		created_by=request.POST.get('created_by')
		new_order = Order(created_by=created_by,isapprovedbydphead=False,isapprovedbysupervisor=False,isapprovedbystoreman=False)
		new_order.save()
		return redirect(reverse("account:Create_Order"))
	else:
		object_created = Order.objects.all()
		return render(request,"Create_Order.html",{"object_created":object_created})

# Delete Function for Delete in Create_Order
def delete_Create_Order(request,id):
	item= Order.objects.get(pk=id)
	item.delete()
	return redirect(reverse('account:Create_Order'))

# Function for Viewing Details
# Html Template:onlyview.html
def onlyviewdetails(request,id):
	items=Item.objects.filter(Order_id=id )
	total=0
	for item in items:
		total+=item.amount
		print(item.name)
	context = {
		"items":items,
		"total":total,
		}
	return render(request,"onlyview.html",context)

# Function for Display of list approved by supervisor in Section of Displaying list
# Html Template:list.html
def get_listdphead(request,id):
    items=Item.objects.filter(Order_id=id )
    total=0
    Total_Budjet=0
    Remaining_Budjet=0
    Remained_Budjet=0
    for item in items:
    	total+=item.amount
    budjets=Stock.objects.filter(Departmentcode=1001)
    for budjet in budjets:
    	Total_Budjet=budjet.Budjet_alloted_peryear
    	Remaining_Budjet=budjet.Budjet_remained
    Remained_Budjet=((Remaining_Budjet)-(total))
    orders=Order.objects.all().filter(isapprovedbysupervisor=True)
    if request.method == 'POST':
    	ids = request.POST.get('Order_id')
    	isapprovedbydphead=request.POST.get('isapprovedbydphead')
    	Order.objects.filter(pk=ids).update(isapprovedbydphead=isapprovedbydphead)
    	return redirect(reverse("account:index"))
    context = {
    	"orders":orders,
    	"items":items,
    	"total":total,
    	"RemainingBudjet":Remaining_Budjet,
    	"Total_Budjet":Total_Budjet,
    	"RemainedBudjet":Remained_Budjet,
    	}
    return render(request,"list.html",context)

# Delete Function for Delete in get_listdphead
def deleteItem_dphead(request,item_id,order_id):
	item = Item.objects.all().filter(pk=item_id)
	print(item)
	item.delete()
	return redirect(reverse('account:get-listdphead',kwargs={"id":order_id}))

# Edit Function for Edit in get_listdphead
# Html Template:edit_list.html
def edit_Item_dphead(request,item_id,order_id):
	if request.method == 'POST':
		item = Item.objects.get(pk=item_id)
		item_code=item.item_code
		quantity = request.POST.get('quantity')
		items=MS_list.objects.get(Itemcode=item_code)
		if items.quantity < float(quantity):
			messages.error(request,"Quantity available:{}".format(items.quantity))
			return redirect(reverse("account:edit_Item_dphead",kwargs={"order_id":order_id,"item_id":item_id}))
		order_id=item.Order_id
		Item_name=item.name
		rate=item.rate
		amount =float(rate)*float(quantity)
		Item.objects.filter(pk=item_id).update(name=Item_name,item_code=item_code,quantity=quantity,rate=rate,amount=amount,Order_id=order_id)
		return redirect(reverse("account:edit_Item_dphead",kwargs={"order_id":order_id,"item_id":item_id}))
	else:
		item = Item.objects.get(pk=item_id)
		return render(request,"edit_list.html",{"item":item})


# Function for Display of list approved by DepartmentHead in Section of Displaying list
# Html Template:storelist.html
def get_liststoreman(request,id):
	items=Item.objects.filter(Order_id=id)
	total=0
	for item in items:
		total+=item.amount
	budjets=Stock.objects.filter(Departmentcode=1001)
	Total_Budjet=0
	Remaining_Budjet=0
	Remained_Budjet=0
	for budjet in budjets:
		Total_Budjet=budjet.Budjet_alloted_peryear
		Remaining_Budjet=budjet.Budjet_remained
		Remained_Budjet=((Remaining_Budjet)-(total))
	if request.method == 'POST':
		ids = request.POST.get('Order_id')
		isapprovedbystoreman=request.POST.get('isapprovedbystoreman')
		Order.objects.filter(pk=ids).update(isapprovedbystoreman=isapprovedbystoreman)
		# items=Item.objects.filter(Order_id=id)
		for item in items:
			item_code_of_Item=item.item_code
			quantity_of_Item=item.quantity
			quantity_in_stock=MS_list.objects.get(Itemcode=item.item_code).quantity
			updated_quantity= ((quantity_in_stock)-(quantity_of_Item))
			MS_list.objects.filter(Itemcode=item_code_of_Item).update(quantity=updated_quantity)
		Stock.objects.filter(pk=1001).update(Budjet_remained=Remained_Budjet)
		return redirect(reverse("account:index"))
	
	# itemss=Item.objects.filter(Order_id=id)
	totals=0
	items_copy=[]
	temp={}
	for item in items:
		temp["pk"]=item.pk
		temp["name"]=item.name
		temp["item_code"]=item.item_code
		temp["quantity"]=item.quantity
		temp["rate"]=item.rate
		temp["amount"]=item.amount
		temp["Order_id"]=item.Order_id
		temp["quantity_in_stock"]=MS_list.objects.get(Itemcode=item.item_code).quantity
		items_copy.append(temp)
		temp={}
		totals+=item.amount
	orders=Order.objects.all()
	context = {
    	"orders":orders,
    	"items":items_copy,
    	"totals":totals,
    	"RemainingBudjet":Remaining_Budjet,
    	"Total_Budjet":Total_Budjet,
    	}
	return render(request,"storelist.html",context)

# Delete Function for Delete in get_liststoreman
def deletebystoreman(request,item_id,order_id):
	item_delete= Item.objects.get(pk=item_id)
	item_delete.delete()
	return redirect(reverse('account:get-liststoreman',kwargs={"id":order_id}))

def edit_item_storeman(request,order_id,item_id):
	if request.method == 'POST':
		item = Item.objects.get(pk=item_id)
		item_code=item.item_code
		quantity = request.POST.get('quantity')
		items=MS_list.objects.get(Itemcode=item_code)
		if items.quantity < float(quantity):
			messages.error(request,"Quantity available:{}".format(items.quantity))
			return redirect(reverse("account:edit_Item_dphead",kwargs={"order_id":order_id,"item_id":item_id}))
		rate=item.rate
		amount =float(rate)*float(quantity)
		Item.objects.filter(pk=item_id).update(item_code=item_code,quantity=quantity,amount=amount)		
		return redirect(reverse('account:edit_item_storeman',kwargs={"order_id":order_id,"item_id":item_id}))
	else:
		item= Item.objects.get(pk=item_id)
		return render(request,"edit_list_storeman.html",{"item":item})


# Html Template:Update_Stock.html# Function For Updating the Stock

def Update_Stock(request):
	if request.method == 'POST':
		Itemcode=request.POST.get('Itemcode')
		quantity = request.POST.get('quantity')
		rate = request.POST.get('rate')
		MS_list.objects.filter(pk=Itemcode).update(quantity=quantity,price=rate)
		# new_stock = Ms_list(Itemname=Itemname,quantity=quantity,rate=rate,Itemcode=Itemcode)
		# new_stock.save()
		return redirect(reverse("account:Update_Stock"))
	else:
		stock_list = MS_list.objects.all()
		context = {
    	"Stock_list":stock_list,
    	}
		return render(request,"Update_Stock.html",context)

# Delete Function for Delete in Update_Stock
def delete_Update_Stock(request,id):
	item= MS_list.objects.get(pk=id)
	item.delete()
	return redirect(reverse('account:Update_Stock'))

# Function For Editing the updated  Stock
# Html Template:edit_Update_Stock.html
def edit_Update_Stock(request,item_codes):
	if request.method == 'POST':
		# item = Item.objects.get(pk=item_codes)
		# item_code=item.item_code
		quantity = request.POST.get('quantity')
		rate = request.POST.get('rate')
		# items=MS_list.objects.get(Itemcode=item_code)
		MS_list.objects.filter(Itemcode=item_codes).update(quantity=quantity,price=rate)
		return redirect(reverse('account:edit_Update_Stock',kwargs={"item_codes":item_codes}))
	else:
		item = MS_list.objects.get(Itemcode=item_codes)
		context = {
		"item":item,
    	}
		return render(request,"edit_Update_Stock.html",context)

