from django.shortcuts import render,redirect

# Create your views here.
from django.views import View
from .models import *
from .forms import *
from shop.forms import *
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
# Create your views here.

class ProductListView(View):
    def get(self,request):
        products=Product.objects.all() #charger la liste des produits à partir de la base de données
        return render(request,"dashboard/product_list.html",{'products':products})
class CategoryListView(View):
    def get(self,request):
        categories=Category.objects.all() #charger la liste des catégories à partir de la base de données
        return render(request,"dashboard/category_list.html",{'categories':categories})

class OrderListView(View):
    def get(self,request):
        commandes=Order.objects.all() #charger la liste des catégories à partir de la base de données
        return render(request,"dashboard/order_list.html",{'commandes':commandes})
class ProductView(View):
    def get(self,request):
        form=ProductForm() #créer un formulaire vide
        return render(request,"dashboard/product_from.html",{'form':form})
    def post(self,request):
        form=ProductForm(request.POST,request.FILES) # récupérer les données saisies dans le formulaire
        if form.is_valid(): # valider les données saisies
            form.save()   # sauvegarder les données dans la base de données
        return  redirect("dashboard:productList")

class ProductUpdateView(View):
    def get(self,request,idp):
        product=Product.objects.get(id=idp)
        form=ProductForm(instance=product) #créer un formulaire vide
        return render(request,"dashboard/product_from.html",{'form':form})
    def post(self,request,idp):
        prouct=Product.objects.get(id=idp)
        form=ProductForm(request.POST,request.FILES,instance=prouct) # récupérer les données saisies dans le formulaire
        if form.is_valid(): # valider les données saisies
            form.save()   # sauvegarder les données dans la base de données
        return  redirect("dashboard:productList")
class ProductDeleteView(View):
    def get(self,request,idp):
        return render(request,"dashboard/delete_confirm.html",{})
    def post(self,request,idp):
        prouct=Product.objects.get(id=idp)
        prouct.delete()
        return  redirect("dashboard:productList")

class ProductDetailsView(View):
    def get(self,request,idp):
        product=Product.objects.get(id=idp)
        return render(request,"dashboard/product_details.html",{'product':product})

class CategoryView(View):
    def get(self,request):
        form=CategoryForm() #créer un formulaire vide
        return render(request,"dashboard/category_from.html",{'form':form})
    def post(self,request):
        form=CategoryForm(request.POST,request.FILES) # récupérer les données saisies dans le formulaire
        if form.is_valid(): # valider les données saisies
            form.save() # sauvegarder les données dans la base de données
        return  redirect("dashboard:categoryList")

class IndexView(View):
    def get(self,request):
        return render(request,"dashboard/index.html",{})

class AddAdminUserView(View):
    def get(self,request):
        user_form = UserForm()
        admin_form = AdminUserForm(request.POST)
        return render(request,'dashboard/register.html',{'user_form': user_form,'admin_form':admin_form})
    def post(self,request):
        user_form = UserForm(request.POST)
        admin_form = AdminUserForm(request.POST,request.FILES)

        if user_form.is_valid() and admin_form.is_valid():
            # Créez un nouvel objet utilisateur mais évitez de l'enregistrer pour le moment
            new_user = user_form.save(commit=False)
            # Définir le mot de passe choisi
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_admin=True
            # Enregistrer l'objet Utilisateur
            new_user.save()
            new_admin=admin_form.save(commit=False)
            new_admin.user=new_user
            new_admin.save()
            return render(request,'dashboard/register_done.html',{'new_user': new_user})
        return HttpResponse('Données invalides')

def AdminUserListView(request):
        adminUsers=AdminUser.objects.all() 
        return render(request,"dashboard/admin_users_list.html",{'adminUsers':adminUsers})

class User_login(View):
    def get(self,request):
        form = LoginForm()
        return render(request, 'dashboard/login.html', {'form': form})
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard:productList')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        return redirect("dashboard:home")

def user_logout(request):
    logout(request)
    return redirect('dashboard:home')

