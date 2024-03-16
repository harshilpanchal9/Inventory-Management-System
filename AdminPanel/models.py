import re
from django.contrib.auth import authenticate, login
import datetime
import os
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
# Create your models here.

# For Admin login
class AdminLogin(models.Model):
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def ValidUser(request, email, password):
        try:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    request.session['email'] = email
                    return redirect('/')
                else:
                    # User is a regular user
                    login(request, user)
                    return redirect('dashboard')
        except Exception as e:
            print(e)

# ------------- Start Category Section --------------

class CategoryModel(models.Model):
    categoryname = models.CharField(max_length=100)

    def addCategory(request):
        if request.method == "POST":
            categoryname = request.POST.get('categoryname')
            if CategoryModel.objects.filter(Q(categoryname__iexact=categoryname.strip())):
                messages.warning(request, "Category name is already exists, please try to choose different Category name!!!")
            else:
                isAddCategory = CategoryModel(categoryname=categoryname)
                isAddCategory.save()
                messages.success(request, "New Category added succussfully.")
                return redirect('/add-category')

    def updateCategory(request):
        try:
            if request.method == "POST":
                categoryname = request.POST.get('old_categoryname')
                categoryId = request.POST.get('categoryId')
                try:
                    category = CategoryModel.objects.get(Q(categoryname__iexact=categoryname))
                    if not category:
                        print("inside cat")
                        new_categoryname = request.POST.get('new_categoryname')
                        CategoryModel.objects.filter(pk=categoryId).update(categoryname=new_categoryname)
                        return True
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

    def deleteCategory(request):
        try:
            categoryid = request.POST.get('categoryid')
            category = CategoryModel.objects.get(pk=categoryid)
            category.delete()
            return True
        except Exception as e:
            print(e)

    def __str__(self):
        return self.categoryname

# ------------- End Category Section --------------

# ------------- Start Product Section --------------
class ProductModel(models.Model):
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    productid = models.IntegerField(default=0, primary_key=True)
    productname = models.CharField(max_length=100, default="Not set")
    productsize = models.CharField(max_length=100, default="Not set")
    productcolor = models.CharField(max_length=100, default="Not set")
    productmaterial = models.CharField(max_length=100, default="Not set")
    purchaseprice = models.IntegerField(default=0, null=True)
    sellprice = models.IntegerField(default=0, null=True)
    productstock = models.IntegerField(default=0, null=True)
    productdesc = models.CharField(max_length=900, default="Not set", null=True)
    quantity_sold = models.IntegerField(null=True, default=0) # This is for finding out 6 top selling products
    productimage = models.ImageField(upload_to='images/product-images', null=True)

    # For adding the New Product
    def addProduct(request):
        try:
            if request.method == 'POST':
                productname = request.POST.get('productname')
                if not productname:
                    return redirect("/add-product")
                elif ProductModel.objects.filter(Q(productname__iexact=productname.strip())):
                    print("Productname is already exists, please choose another name.")
                    messages.warning(request, "Product name is already exists, please try to choose different product name!!!")
                    return redirect("/add-product")
                else:
                    productsize = request.POST.get('productsize')
                    productcolor = request.POST.get('productcolor')
                    productmaterial = request.POST.get('productmaterial')
                    purchaseprice = int(request.POST.get('purchaseprice'))
                    sellprice = int(request.POST.get('sellprice'))
                    productstock = int(request.POST.get('productstock'))
                    productdesc = request.POST.get('productdesc')
                    productimage = request.FILES.get('productimage')
                    
                    # To check the extension of image
                    if productimage:
                        if not productimage.name.endswith(('.jpg', '.jpeg', '.png')):
                            messages.warning(request,"This Product form accepts only (jpg,jpeg,png) images.")
                            return redirect('add-product')

                    # For categoryname entry:
                    categoryId = int(request.POST.get('categories'))
                    category_name = None
                    all_categories = CategoryModel.objects.all()
                    for category in all_categories:
                        if category.id == categoryId:
                            category_name = category.categoryname
                    category = CategoryModel.objects.get(categoryname=category_name)

                    if ProductModel.objects.all():
                        lastProductId = ProductModel.objects.all().last().__getattribute__("productid")
                        newProductId = lastProductId + 1
                    else:
                        newProductId = 1001
                    Addproduct = ProductModel(category=category, productid=newProductId, productname=productname, productsize=productsize, productcolor=productcolor,
                                              productmaterial=productmaterial, purchaseprice=purchaseprice, sellprice=sellprice, productstock=productstock, productdesc=productdesc, productimage=productimage)
                    Addproduct.save()
                    messages.success(request,"New Product added succussfully.")
                    context = {'productid2': newProductId+1, 'flag': 1}
                    return render(request, "add-product.html", context)
        except Exception as e:
            print(e)

    def updateProduct(request):
        try:
            if request.method == "POST":
                productimage = request.FILES.get('productimage')
                old_productimage = request.POST.get('old_productimage')
                imagepath = ""
                
                # For updating the image path
                if productimage and productimage != old_productimage:
                    filename = os.path.basename(productimage.name)
                    imagepath = "images/product-images/" + filename
                    fs = FileSystemStorage()
                    fs.save(imagepath, productimage)
                    productimage = imagepath

                # To delete a existing image before adding new one.
                productid = request.POST.get('productid')
                product = ProductModel.objects.get(pk=productid)
                if productimage and old_productimage and productimage != old_productimage:
                    # Delete the existing image file if it exists
                    if product.productimage:
                        product.productimage.delete()
                    # Set the new image file for the product
                    product.productimage = productimage
                    
                    # Save the product to update the changes
                    product.save()

                # For categoryname entry
                categoryId = int(request.POST.get('categories'))
                
                try:
                    flag = 0                    
                    new_productname = request.POST.get('new_productname')
                    new_productsize = request.POST.get('new_productsize')
                    new_productcolor = request.POST.get('new_productcolor')
                    new_productmaterial = request.POST.get('new_productmaterial')
                    new_purchaseprice = int(request.POST.get('new_purchaseprice'))
                    new_sellprice = int(request.POST.get('new_sellprice'))
                    new_productstock = int(request.POST.get('new_productstock'))
                    new_productdesc = request.POST.get('new_productdesc')
                    if productimage:
                        ProductModel.objects.filter(pk=productid).update(
                            category = categoryId,
                            productname = new_productname,
                            productsize = new_productsize,
                            productcolor = new_productcolor,
                            productmaterial = new_productmaterial,
                            purchaseprice = new_purchaseprice,
                            sellprice = new_sellprice,
                            productstock = new_productstock,
                            productdesc = new_productdesc,
                            productimage = productimage
                        )
                    else:
                        ProductModel.objects.filter(pk=productid).update(
                            category = categoryId,
                            productname = new_productname,
                            productsize = new_productsize,
                            productcolor = new_productcolor,
                            productmaterial = new_productmaterial,
                            purchaseprice = new_purchaseprice,
                            sellprice = new_sellprice,
                            productstock = new_productstock,
                            productdesc = new_productdesc,
                        )
                    return flag
                except ProductModel.DoesNotExist:
                    messages.warning(request, "Product does not exist.")
        except Exception as e:
            print(e)

    def deleteProduct(request):
        try:
            productid = request.POST.get('productid')
            product = ProductModel.objects.get(pk=productid)
            product.delete()
            return True
        except Exception as e:
            print(e)

    def __str__(self):
        return self.productname
    
    
# ------------- Supplier Section starts --------------

class Suppliers(models.Model):
    supplierId = models.IntegerField(default=1001, primary_key=True)
    supplierName = models.CharField(max_length=100, default="Not set")
    supplierGst = models.CharField(max_length=100, default="Not set")
    supplierAddress = models.CharField(max_length=100, default="Not available")
    supplierEmail = models.CharField(max_length=100, default="Not set")
    supplierPhone = models.CharField(max_length=100, default="Not set")

    def __str__(self):
        return self.supplierName

    class Meta:
        verbose_name_plural = "Suppliers"

    def addSupplier(self, supplierId, supplierName, supplierGst, supplierAddress, supplierEmail, supplierPhone):
        print("supplierId: ", supplierId)
        self.supplierId = supplierId
        self.supplierName = supplierName
        self.supplierGst = supplierGst
        self.supplierAddress = supplierAddress
        self.supplierEmail = supplierEmail
        self.supplierPhone = supplierPhone

        try:
            self.save()
            return True
        except Exception as e:
            print(e)
            return False

    def deleteSupplier(request):
        try:
            supplierId = request.POST.get('supplierId')
            print("supplierId",supplierId)
            supplier = Suppliers.objects.get(pk=supplierId)
            supplier.delete()
            return True
        except Exception as e:
            print(e)

    def generateSupplierId():
        if Suppliers.objects.all():
            lastSupplierId = Suppliers.objects.all().last().supplierId
            print("lastSupplierId: ", lastSupplierId)
            newSupplierId = lastSupplierId + 1
        else:
            newSupplierId = 1001
        return newSupplierId

# ------------- Supplier Expense Section Starts --------------
class SupplierExpenses(models.Model):
    billNo = models.IntegerField(default=0000, primary_key=True)
    expenseType = models.CharField(max_length=100)
    billDate = models.DateField(default=datetime.date.today)
    supplierName = models.CharField(max_length=100)
    supplierPhone = models.CharField(max_length=12)
    supplierGst = models.CharField(max_length=50)
    paymentType = models.CharField(max_length=10)
    total = models.FloatField()
    gst = models.FloatField(default=0)
    grossTotal = models.FloatField(default=0)
    description = models.CharField(max_length=100)

    def generateBillNo():
        if SupplierExpenses.objects.all():
            lastBillNo = SupplierExpenses.objects.all().last().billNo
            newBillNo = lastBillNo + 1
        else:
            newBillNo = 1001
        return newBillNo

    def __str__(self):
        return str(self.billNo)

    class Meta:
        verbose_name_plural = "Supplier Expenses"

    def addSupplierExpenses(self, request):
        self.billNo = request.POST.get('billNo')
        self.expenseType = request.POST.get('expenseType')
        self.billDate = request.POST.get('billDate')
        self.supplierName = Suppliers.objects.get(supplierId=request.POST.get('supplier')).supplierName
        self.supplierPhone = request.POST.get('supplierPhone')
        self.supplierGst = request.POST.get('supplierGst')
        self.paymentType = request.POST.get('paymentType')
        self.total = float(request.POST.get('total'))
        self.gst = float(request.POST.get('gst'))
        self.grossTotal = float(request.POST.get('grossTotal'))
        self.description = request.POST.get('description')
        try:
            self.save()
            return True
        except Exception as e:
            print(e)
            return False
        
class SupplierExpensesProducts(models.Model):
    id = models.AutoField(primary_key=True)
    billNo = models.ForeignKey(SupplierExpenses, on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=50)
    pricePerUnit = models.FloatField()
    amount = models.FloatField()

    def __str__(self):
        return str(self.billNo)

    class Meta:
        verbose_name_plural = "Supplier Expenses Products"

    def addSupplierExpensesProduct(self, request, rowNumber):
        self.billNo = SupplierExpenses.objects.get(billNo=request.POST.get('billNo'))
        self.product = request.POST.get(f'product_{rowNumber}')
        self.quantity = request.POST.get(f'quantity_{rowNumber}')
        self.unit = request.POST.get(f'unit_{rowNumber}')
        self.pricePerUnit = request.POST.get(f'pricePerUnit_{rowNumber}')
        self.amount = request.POST.get(f'amount_{rowNumber}')

        try:
            self.save()
            return True
        except Exception as e:
            print(e)
            return False
# ------------- Supplier Expense Section Ends --------------

# ------------- Purchase Section starts --------------

class Purchases(models.Model):
    billNo = models.IntegerField(default=0000, primary_key=True)
    billDate = models.DateField(default=datetime.date.today)
    supplierId = models.IntegerField(default=0)
    supplierName = models.CharField(max_length=100)
    supplierPhone = models.CharField(max_length=12)
    supplierGst = models.CharField(max_length=50)
    paymentType = models.CharField(max_length=10)
    total = models.FloatField()
    gst = models.FloatField(default=0)
    otherExpenses = models.FloatField(default=0)
    grossTotal = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    netTotal = models.FloatField(default=0)
    paidAmount = models.FloatField(default=0)
    description = models.CharField(max_length=100)
    billImage = models.ImageField(upload_to='images/purchase-bills', null=True)
    paymentStatus = models.CharField(max_length=50,default="Paid")

    def generateBillNo():
        if Purchases.objects.all():
            lastBillNo = Purchases.objects.all().last().billNo
            newBillNo = lastBillNo + 1
        else:
            newBillNo = 1001
        return newBillNo

    def __str__(self):
        return str(self.billNo)

    class Meta:
        verbose_name_plural = "Purchases"

    def addPurchase(self, request):
        self.billNo = request.POST.get('billNo')
        self.billDate = request.POST.get('billDate')
        self.supplierId = request.POST.get('supplier')
        self.supplierName = Suppliers.objects.get(supplierId=request.POST.get('supplier')).supplierName
        self.supplierPhone = request.POST.get('supplierPhone')
        self.supplierGst = request.POST.get('supplierGst')
        self.paymentType = request.POST.get('paymentType')
        self.total = float(request.POST.get('total'))
        self.gst = float(request.POST.get('gst'))
        self.otherExpenses = float(request.POST.get('otherExpenses')) if request.POST.get('otherExpenses') else 0.0
        self.grossTotal = float(request.POST.get('grossTotal'))
        self.discount = float(request.POST.get('discount')) if request.POST.get('discount') else 0.0
        self.netTotal = float(request.POST.get('netTotal'))
        self.paidAmount = float(request.POST.get('paidAmount')) if request.POST.get('paidAmount') else 0.0
        self.description = request.POST.get('description')
        self.billImage = request.FILES.get('upload-bill')

        if self.paidAmount == 0.0:
            self.paymentStatus = "Full Credit"
        elif self.paidAmount < self.netTotal:
            self.paymentStatus = "Partial Credit"
        elif self.paidAmount == self.netTotal:
            self.paymentStatus = "Paid"
        
        try:
            print('SupplierName: ', self.supplierName)
            self.save()
            return True
        except Exception as e:
            print(e)
            return False

class PurchasedProducts(models.Model):
    id = models.AutoField(primary_key=True)
    billNo = models.ForeignKey(Purchases, on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=50)
    pricePerUnit = models.FloatField(default=0)
    amount = models.FloatField(default=0)

    def __str__(self):
        return str(self.billNo)

    class Meta:
        verbose_name_plural = "Purchased Products"

    def addPurchasedProduct(self, request, rowNumber):
        self.billNo = Purchases.objects.get(billNo=request.POST.get('billNo'))
        self.product = request.POST.get(f'product_{rowNumber}')
        self.quantity = request.POST.get(f'quantity_{rowNumber}')
        self.unit = request.POST.get(f'unit_{rowNumber}')
        self.pricePerUnit = request.POST.get(f'pricePerUnit_{rowNumber}')
        self.amount = request.POST.get(f'amount_{rowNumber}')

        try:
            self.save()
            return True
        except Exception as e:
            print(e)
            return False

class OtherExpensesOfPurchase(models.Model):
    id = models.AutoField(primary_key=True)
    billNo = models.ForeignKey(Purchases, on_delete=models.CASCADE)
    expenseType = models.CharField(max_length=50)
    amount = models.FloatField(default=0)

    def addExpense(self, request, rowNumber):
        self.billNo = Purchases.objects.get(billNo=request.POST.get('billNo'))
        self.expenseType = request.POST.get(f'expenseType_{rowNumber}')
        self.amount = request.POST.get(f'expenseAmount_{rowNumber}')

        try:
            self.save()
            return True
        except Exception as e:
            print(e)
            return False
        
    def __str__(self):
        return str(self.billNo)

    class Meta:
        verbose_name_plural = "Other expenses of purchases"

# ------------- Sale Section -----------------------

class Sells(models.Model):
    billNo = models.IntegerField(default=0000, primary_key=True)
    billDate = models.DateField(default=datetime.date.today)
    customerId = models.IntegerField(default=0000)
    customerName = models.CharField(max_length=100)
    customerPhone = models.CharField(max_length=12)
    customerGst = models.CharField(max_length=50)
    paymentType = models.CharField(max_length=10)
    total = models.FloatField()
    gst = models.FloatField(default=0)
    otherExpenses = models.FloatField(default=0)
    grossTotal = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    netTotal = models.FloatField(default=0)
    paidAmount = models.FloatField(default=0)
    description = models.CharField(max_length=100)
    billImage = models.ImageField(upload_to='images/purchase-bills', null=True)
    paymentStatus = models.CharField(max_length=50,default="Paid")

    def generateBillNo():
        if Sells.objects.all():
            lastBillNo = Sells.objects.all().last().billNo
            newBillNo = lastBillNo + 1
        else:
            newBillNo = 1001
        return newBillNo

    def __str__(self):
        return str(self.billNo)

    class Meta:
        verbose_name_plural = "Sells"

    def addSell(self, request):
        self.billNo = request.POST.get('billNo')
        self.billDate = request.POST.get('billDate')
        self.customerId = request.POST.get('customer')
        self.customerName = Customers.objects.get(
        customerId=request.POST.get('customer')).customerName
        self.customerPhone = request.POST.get('customerPhone')
        self.customerGst = request.POST.get('customerGst')
        self.paymentType = request.POST.get('paymentType')
        self.total = float(request.POST.get('total'))
        self.gst = float(request.POST.get('gst'))
        self.otherExpenses = float(request.POST.get('otherExpenses')) if request.POST.get('otherExpenses') else 0.0
        self.grossTotal = float(request.POST.get('grossTotal'))
        self.discount = float(request.POST.get('discount')) if request.POST.get('discount') else 0.0
        self.netTotal = float(request.POST.get('netTotal'))
        self.paidAmount = float(request.POST.get('paidAmount')) if request.POST.get('paidAmount') else 0.0
        self.description = request.POST.get('description')
        self.billImage = request.FILES.get('upload-bill')

        if self.paidAmount == 0.0:
            self.paymentStatus = "Full Credit"
        elif self.paidAmount < self.netTotal:
            self.paymentStatus = "Partial Credit"
        elif self.paidAmount == self.netTotal:
            self.paymentStatus = "Paid"

        try:
            self.save()
            return True
        except Exception as e:
            print(e)
            return False


class SoldProducts(models.Model):
    id = models.AutoField(primary_key=True)
    billNo = models.ForeignKey(Sells, on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=50)
    pricePerUnit = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    
    def __str__(self):
        return str(self.billNo)

    class Meta:
        verbose_name_plural = "Sold Products"

    def addSoldProduct(self, request, rowNumber):
        self.billNo = Sells.objects.get(billNo=request.POST.get('billNo'))
        self.product = request.POST.get(f'product_{rowNumber}')
        self.quantity = request.POST.get(f'quantity_{rowNumber}')
        self.unit = request.POST.get(f'unit_{rowNumber}')
        self.pricePerUnit = request.POST.get(f'pricePerUnit_{rowNumber}')
        self.amount = request.POST.get(f'amount_{rowNumber}')
        product_name = ProductModel.objects.get(productname = self.product)
        available_stock = product_name.productstock
        updated_stock = available_stock - int(self.quantity)
        quantity_sold = product_name.quantity_sold + int(self.quantity)

        try:
            product_name.quantity_sold = quantity_sold
            product_name.productstock = updated_stock
            product_name.save()
            self.save()
            return True
        except Exception as e:
            print(e)
            return False
        
class OtherExpensesOfSells(models.Model):
    id = models.AutoField(primary_key=True)
    billNo = models.ForeignKey(Sells, on_delete=models.CASCADE)
    expenseType = models.CharField(max_length=50)
    amount = models.FloatField(default=0)

    def addExpense(self, request, rowNumber):
        self.billNo = Sells.objects.get(billNo=request.POST.get('billNo'))
        self.expenseType = request.POST.get(f'expenseType_{rowNumber}')
        self.amount = request.POST.get(f'expenseAmount_{rowNumber}')

        try:
            self.save()
            return True
        except Exception as e:
            print(e)
            return False
        
    def __str__(self):
        return str(self.billNo)

    class Meta:
        verbose_name_plural = "Other expenses of sells"

# ------------- Customer Section -------------------

class Customers(models.Model):
    customerId = models.IntegerField(default=1001, primary_key=True)
    customerName = models.CharField(max_length=100, default="Not set")
    customerGst = models.CharField(max_length=100, default="Not set")
    customerAddress = models.CharField(max_length=100, default="Not available")
    customerEmail = models.CharField(max_length=100, default="Not set")
    customerPhone = models.CharField(max_length=100, default="Not set")

    def __str__(self):
        return self.customerName

    class Meta:
        verbose_name_plural = "Customers"

    def addCustomer(self, customerId, customerName, customerGst, customerAddress, customerEmail, customerPhone):
        self.customerId = customerId
        self.customerName = customerName
        self.customerGst = customerGst
        self.customerAddress = customerAddress
        self.customerEmail = customerEmail
        self.customerPhone = customerPhone

        try:
            self.save()
            return True
        except Exception as e:
            print(e)
            return False

    def deleteCustomer(request):
        try:
            customerId = request.POST.get('customerId')
            print("customerId",customerId)
            customer = Customers.objects.get(pk=customerId)
            customer.delete()
            return True
        except Exception as e:
            print(e)

    def generateCustomerId():
        if Customers.objects.all():
            lastCustomerId = Customers.objects.all().last().customerId
            newCustomerId = lastCustomerId + 1
        else:
            newCustomerId = 1001
        return newCustomerId
    
# ------------- Customer Expense Section Starts --------------

class CustomerExpenses(models.Model):
    billNo = models.IntegerField(default=0000, primary_key=True)
    expenseType = models.CharField(max_length=100)
    billDate = models.DateField(default=datetime.date.today)
    customerName = models.CharField(max_length=100)
    customerPhone = models.CharField(max_length=12)
    customerGst = models.CharField(max_length=50)
    paymentType = models.CharField(max_length=10)
    total = models.FloatField()
    gst = models.FloatField(default=0)
    grossTotal = models.FloatField(default=0)
    description = models.CharField(max_length=100)

    def generateBillNo():
        if CustomerExpenses.objects.all():
            lastBillNo = CustomerExpenses.objects.all().last().billNo
            newBillNo = lastBillNo + 1
        else:
            newBillNo = 1001
        return newBillNo

    def __str__(self):
        return str(self.billNo)

    class Meta:
        verbose_name_plural = "Customer Expenses"

    def addCustomerExpenses(self, request):
        self.billNo = request.POST.get('billNo')
        self.expenseType = request.POST.get('expenseType')
        self.billDate = request.POST.get('billDate')
        self.customerName = Customers.objects.get(customerId=request.POST.get('customer')).customerName
        self.customerPhone = request.POST.get('customerPhone')
        self.customerGst = request.POST.get('customerGst')
        self.paymentType = request.POST.get('paymentType')
        self.total = float(request.POST.get('total'))
        self.gst = float(request.POST.get('gst'))
        self.grossTotal = float(request.POST.get('grossTotal'))
        self.description = request.POST.get('description')
        try:
            self.save()
            return True
        except Exception as e:
            print(e)
            return False
        
class CustomerExpensesProducts(models.Model):
    id = models.AutoField(primary_key=True)
    billNo = models.ForeignKey(CustomerExpenses, on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=50)
    pricePerUnit = models.FloatField()
    amount = models.FloatField()

    def __str__(self):
        return str(self.billNo)

    class Meta:
        verbose_name_plural = "Customer Expenses Products"

    def addCustomerExpensesProduct(self, request, rowNumber):
        self.billNo = CustomerExpenses.objects.get(billNo=request.POST.get('billNo'))
        self.product = request.POST.get(f'product_{rowNumber}')
        self.quantity = request.POST.get(f'quantity_{rowNumber}')
        self.unit = request.POST.get(f'unit_{rowNumber}')
        self.pricePerUnit = request.POST.get(f'pricePerUnit_{rowNumber}')
        self.amount = request.POST.get(f'amount_{rowNumber}')

        try:
            self.save()
            return True
        except Exception as e:
            print(e)
            return False
# ------------- Customer Expense Section Ends --------------

# ------------- Supplier Due payments starts --------------
class SuppliersDuePayments():
    def __init__(self):
        self.supplierId = 0
        self.supplierName = ''
        self.supplierGst = ''
        self.supplierPhone = ''
        self.paidAmount = 0
        self.dues = 0
        self.totalAmount = 0

    def getDuePayments():
        allDuePayments = list()

        totalAmount = 0
        totalDuePayments = 0
        totalPaidAmount = 0
        for supplier in Suppliers.objects.all():
            print('sid', supplier.supplierId)
            supplierPurchases = Purchases.objects.filter(supplierId=supplier.supplierId)
            print('sp', supplierPurchases)
            for supplierPurchase in supplierPurchases:
                duePayment = SuppliersDuePayments()
                duePayment.supplierId = supplierPurchase.supplierId
                duePayment.supplierName = supplierPurchase.supplierName
                duePayment.supplierGst = supplierPurchase.supplierGst
                duePayment.supplierPhone = supplierPurchase.supplierPhone
                totalAmount += supplierPurchase.netTotal
                totalPaidAmount += supplierPurchase.paidAmount
                totalDuePayments += (supplierPurchase.netTotal - supplierPurchase.paidAmount)

                if totalAmount > 0:
                    duePayment.totalAmount = round(totalAmount, 2)
                    duePayment.paidAmount = round(totalPaidAmount, 2)
                    duePayment.dues = round(totalDuePayments, 2) 
    
            duplicate_found = False
            for existing_payment in allDuePayments:
                if (existing_payment.supplierId == duePayment.supplierId):
                    duplicate_found = True
                    break

            if not duplicate_found:
                if totalAmount > 0:
                    allDuePayments.append(duePayment)

            totalAmount = 0
            totalPaidAmount = 0
            totalDuePayments = 0
        return allDuePayments      
                   
# ------------- Supplier Due bills starts --------------
class SuppliersDueBills():
    def __init__(self):
        self.billNo = 0
        self.billDate = ''
        self.supplierId = 0
        self.supplierName = ''
        self.supplierGst = ''
        self.supplierPhone = ''
        self.paidAmount = 0
        self.dues = 0
        self.totalAmount = 0
    
    def clearDues(billNo, supplierId):
        try:
            supplierPurchase = Purchases.objects.get(billNo=billNo, supplierId=supplierId)
            print('sp', supplierPurchase.paidAmount)
            supplierPurchase.paidAmount = supplierPurchase.netTotal
            supplierPurchase.paymentStatus = "Paid"
            print('sp', supplierPurchase.paidAmount)
            supplierPurchase.save()
            return True
        except:
            return False 
        
    def getDueBills(supplierId):
        allDueBills = list()
        print('sid', supplierId)
        supplierPurchases = Purchases.objects.filter(supplierId=supplierId)
        print('sp', supplierPurchases)

        for supplierPurchase in supplierPurchases:
            if supplierPurchase.netTotal != supplierPurchase.paidAmount:
                dueBill = SuppliersDueBills()
                dueBill.billNo = supplierPurchase.billNo
                print('duebill no', dueBill.billNo)

                dueBill.billDate = supplierPurchase.billDate
                dueBill.supplierId = supplierPurchase.supplierId
                dueBill.supplierName = supplierPurchase.supplierName
                dueBill.supplierGst = supplierPurchase.supplierGst
                dueBill.supplierPhone = supplierPurchase.supplierPhone
                dueBill.totalAmount = round(supplierPurchase.netTotal, 2)
                dueBill.dues = round(supplierPurchase.netTotal - supplierPurchase.paidAmount, 2)
                dueBill.paidAmount = round(supplierPurchase.paidAmount, 2)
                allDueBills.append(dueBill)  
        return allDueBills, supplierPurchases[0].supplierName
             
# ------------- Customer Due payments starts --------------
class CustomersDuePayments():
    def __init__(self):
        self.customerId = 0
        self.customerName = ''
        self.customerGst = ''
        self.customerPhone = ''
        self.paidAmount = 0
        self.dues = 0
        self.totalAmount = 0
        
    def getDuePayments():
        allDuePayments = list()

        totalAmount = 0
        totalDuePayments = 0
        totalPaidAmount = 0
        for customer in Customers.objects.all():
            print('cid', customer.customerId)
            customerPurchases = Sells.objects.filter(customerId=customer.customerId)
            print('cp', customerPurchases)
            for customerPurchase in customerPurchases:
                duePayment = CustomersDuePayments()
                duePayment.customerId = customerPurchase.customerId
                duePayment.customerName = customerPurchase.customerName
                duePayment.customerGst = customerPurchase.customerGst
                duePayment.customerPhone = customerPurchase.customerPhone
                totalAmount += customerPurchase.netTotal
                totalPaidAmount += customerPurchase.paidAmount
                totalDuePayments += (customerPurchase.netTotal - customerPurchase.paidAmount)

                if totalAmount > 0:
                    duePayment.totalAmount = round(totalAmount, 2)
                    duePayment.paidAmount = round(totalPaidAmount, 2)
                    duePayment.dues = round(totalDuePayments, 2) 
            
            duplicate_found = False
            for existing_payment in allDuePayments:
                if (existing_payment.customerId == duePayment.customerId):
                    duplicate_found = True
                    break

            if not duplicate_found:
                if totalAmount > 0:
                    allDuePayments.append(duePayment)
            print(allDuePayments)
            totalAmount = 0
            totalPaidAmount = 0
            totalDuePayments = 0
        return allDuePayments         
                   
# ------------- Customer Due bills starts --------------
class CustomersDueBills():
    def __init__(self):
        self.billNo = 0
        self.billDate = ''
        self.customerId = 0
        self.customerName = ''
        self.customerGst = ''
        self.customerPhone = ''
        self.paidAmount = 0
        self.dues = 0
        self.totalAmount = 0

    def clearDues(billNo, customerId):
        try:
            customerPurchase = Sells.objects.get(billNo=billNo, customerId=customerId)
            print('sp', customerPurchase.paidAmount)
            customerPurchase.paidAmount = customerPurchase.netTotal
            customerPurchase.paymentStatus = "Paid"
            print('sp', customerPurchase.paidAmount)
            customerPurchase.save()
            return True
        except:
            return False 
        
    def getDueBills(customerId):
        allDueBills = list()
        print('cid', customerId)
        customerPurchases = Sells.objects.filter(customerId=customerId)
        print('cp', customerPurchases)

        for customerPurchase in customerPurchases:
            if customerPurchase.netTotal != customerPurchase.paidAmount:
                dueBill = CustomersDueBills()
                dueBill.billNo = customerPurchase.billNo
                dueBill.billDate = customerPurchase.billDate
                dueBill.customerId = customerPurchase.customerId
                dueBill.customerName = customerPurchase.customerName
                dueBill.customerGst = customerPurchase.customerGst
                dueBill.customerPhone = customerPurchase.customerPhone
                dueBill.totalAmount = round(customerPurchase.netTotal, 2)
                dueBill.dues = round(customerPurchase.netTotal - customerPurchase.paidAmount, 2)
                dueBill.paidAmount = round(customerPurchase.paidAmount, 2)
                allDueBills.append(dueBill)  
        return allDueBills, customerPurchases[0].customerName