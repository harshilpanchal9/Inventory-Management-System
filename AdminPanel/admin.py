from django.contrib import admin
from AdminPanel.models import AdminLogin, CategoryModel, ProductModel, Suppliers, Purchases, PurchasedProducts, Customers, Sells, SoldProducts, SupplierExpenses, SupplierExpensesProducts, CustomerExpenses, CustomerExpensesProducts, OtherExpensesOfPurchase, OtherExpensesOfSells

# Register your models here.
admin.site.register(AdminLogin)

# Category model autoincrement field
admin.site.register(CategoryModel)

# Product model 
admin.site.register(ProductModel)

# Suppliers
admin.site.register(Suppliers)

# Purchases
admin.site.register(Purchases)

# PurchasedProducts
admin.site.register(PurchasedProducts)

# OtherExpensesOfPurchase
admin.site.register(OtherExpensesOfPurchase)

# Customers
admin.site.register(Customers)

# Sells
admin.site.register(Sells)

# SoldProducts
admin.site.register(SoldProducts)

# OtherExpensesOfSells
admin.site.register(OtherExpensesOfSells)

# SupplierExpenses
admin.site.register(SupplierExpenses)

# SupplierExpensesProducts
admin.site.register(SupplierExpensesProducts)

# CustomerExpenses
admin.site.register(CustomerExpenses)

# CustomerExpensesProducts
admin.site.register(CustomerExpensesProducts)
