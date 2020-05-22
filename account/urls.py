from django.urls import path
from . import views

app_name="account"


urlpatterns = [
	   path("account/getin",views.getin,name="getin"),
	   path("account/register",views.register,name="register"),
	   path("account/getout",views.getout,name="getout"),
	   path("",views.index, name="index"),
	   path("account/Add_Department",views.Add_Department,name="Add_Department"),
	   path("account/Create_Order",views.Create_Order,name="Create_Order"),
	   path("account/Details_Order/<id>",views.get_listsupervisor,name="get-listsupervisor"),
	   path("account/onlyviewdetails/<id>",views.onlyviewdetails,name="onlyviewdetails"),
	   path("account/Update_MSlist",views.Update_MSlist,name="Update_MSlist"),
	   path("account/details/<id>",views.get_listdphead,name="get-listdphead"),
	   path("account/Details/<id>",views.get_liststoreman,name="get-liststoreman"),
	   path("account/Update_Stock",views.Update_Stock,name="Update_Stock"),
	   path("account/delete_in_get_listsupervisor/<id>/<order_id>",views.delete_in_get_listsupervisor,name="delete_in_get_listsupervisor"),
	   path("account/delete_Update_MSlist/<id>",views.delete_Update_MSlist,name="delete_Update_MSlist"),
	   path("account/delete_Add_Department/<id>",views.delete_Add_Department,name="delete_Add_Department"),
	   path("account/delete_Create_Order/<id>",views.delete_Create_Order,name="delete_Create_Order"),
	   path("account/delete_Update_Stock/<id>",views.delete_Update_Stock,name="delete_Update_Stock"),
	   path("account/deletebydphead/<item_id>/<order_id>",views.deleteItem_dphead,name="delete-item_dphead"),
	   path("account/deletebystoreman/<order_id>/<item_id>",views.deletebystoreman,name="delete-item_storeman"),
	   path("account/edit_Update_MSlist/<id>",views.edit_Update_MSlist,name="edit_Update_MSlist"),
	   path("account/edit_Add_Department/<id>",views.edit_Add_Department,name="edit_Add_Department"),
	   path("account/edit_Item_dphead/<item_id>/<order_id>",views.edit_Item_dphead,name="edit_Item_dphead"),
	   path("account/edit_Update_Stock/<item_codes>",views.edit_Update_Stock,name="edit_Update_Stock"),
	   path("account/edit_item_storeman/<order_id>/<item_id>",views.edit_item_storeman,name="edit_item_storeman"),
	   ]