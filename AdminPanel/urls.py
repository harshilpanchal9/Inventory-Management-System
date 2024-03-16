from django.contrib import admin
from django.urls import path, include
from AdminPanel import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.index, name='index'),
    # --------------------- Dashboard -------------------------
    path("dashboard", views.dashboard, name='dashboard'), 
    # --------------------- Category --------------------------
    path("add-category", views.addcategory, name='add-category'),    
    path("view-category", views.viewcategory, name='view-category'),    
    path("edit-category", views.editcategory, name='edit-category'),    
    # --------------------- Product ---------------------------
    path("add-product", views.addproduct, name='add-product'),    
    path("view-products", views.viewproducts, name='view-products'),    
    path("edit-product", views.editproduct, name='edit-product'),    
    # --------------------- Purchase --------------------------
    path("add-purchase", views.addPurchase, name='add-purchase'),    
    path("purchases", views.purchases, name='purchases'),    
    path("view-purchase-bill", views.viewPurchaseBill, name='view-purchase-bill'),     
    path("purchase-return", views.purchaseReturn, name='purchase-return'),     
    # --------------------- Sale ------------------------------
    path("add-sell", views.addSell, name='add-sell'),   
    path("sells", views.sells, name='sells'),    
    path("view-sell-bill", views.viewSellBill, name='view-sell-bill'),   
    path("sell-return", views.sellReturn, name='sell-return'),   
    # --------------------- Customers -------------------------
    path("customers", views.customers, name='customers'),       
    path("add-customer", views.addCustomer, name='add-customer'),        
    path("edit-customer", views.editCustomer, name='edit-customer'),   
    path("get-customer-data", views.getCustomerData, name='getCustomerData'),  
    path("customer-expenses", views.customerExpenses, name='customer-expenses'),  
    path("view-customer-expenses", views.viewCustomerExpenses, name='view-customer-expenses'),  
    path("view-customer-expense-bill", views.viewCustomerExpenseBill, name='view-customer-expense-bill'),  
    # --------------------- Suppliers -------------------------
    path("suppliers", views.suppliers, name='suppliers'),   
    path("add-supplier", views.addSupplier, name='add-supplier'),    
    path("edit-supplier", views.editSupplier, name='edit-supplier'),   
    path("get-supplier-data", views.getSupplierData, name='getSupplierData'),  
    path("supplier-expenses", views.supplierExpenses, name='supplier-expenses'), 
    path("view-supplier-expenses", views.viewSupplierExpenses, name='view-supplier-expenses'), 
    path("view-supplier-expense-bill", views.viewSupplierExpenseBill, name='view-supplier-expense-bill'), 
    # --------------------- Invoice ---------------------------
    path("sell-invoice", views.Sellinvoice, name='sell-invoice'),    
    path("purchase-invoice", views.Purchaseinvoice, name='purchase-invoice'),
    path('generate_excel_for_sell', views.generate_excel_for_sell, name='generate_excel_for_sell'),    
    path('generate_excel_for_purchase', views.generate_excel_for_purchase, name='generate_excel_for_purchase'),    
    path('generate_excel_for_sellBills', views.generate_excel_for_sellBills, name='generate_excel_for_sellBills'),    
    path('generate_excel_for_purchaseBills', views.generate_excel_for_purchaseBills, name='generate_excel_for_purchaseBills'), 
    # --------------------- Accounts ---------------------------  
    path('suppliers-due-payments', views.suppliersDuePayments, name='suppliers-due-payments'),
    path('suppliers-due-bills', views.suppliersDueBills, name='suppliers-due-bills'),
    path('customers-due-payments', views.customersDuePayments, name='customers-due-payments'),
    path('customers-due-bills', views.customersDueBills, name='customers-due-bills'),   
    # --------------------- Support ---------------------------
    path("support", views.support, name='support'),  
    # --------------------- Logout ----------------------------
    path('logout', views.delSession, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)