from django.shortcuts import render,redirect
from django.views import View
from dashboard.models import *
from .forms import *
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

# Create your views here.
class IndexView(View):
    def get(self,request):
        products=Product.objects.all() #charger la liste des produits à partir de la base de données
        cart_product_form = CartAddProductForm()
        return render(request,"shop/product_list.html",{'products':products,'cart_product_form':cart_product_form})

class ProductListView(View):
    def get(self,request):
        products=Product.objects.all() #charger la liste des produits à partir de la base de données
        cart_product_form = CartAddProductForm()
        return render(request,"shop/product_list.html",{'products':products,'cart_product_form':cart_product_form})
class ProductsByCategoryView(View):
    def get(self,request,idc):
        products=Product.objects.filter(category_id=idc)
        return render(request,"shop/product_list.html",{'products':products})
class ProductDetailsView(View):
    def get(self,request,idp):
        product=Product.objects.get(id=idp)
        cart_product_form = CartAddProductForm()

        return render(request,"shop/product_detail.html",{'product':product,'cart_product_form':cart_product_form})

class MyordersView(View):
    def get(self,request):
        customer=Costumer.objects.get(user_id=request.user.id)
        orders=Order.objects.filter(costumer_id=customer.id)
        

        cart_product_form = CartAddProductForm()

        return render(request,"shop/myorders.html",{'orders':orders,'cart_product_form':cart_product_form})

class PaymentView(View):
    def get(self,request,ido):
        form=PaymentForm() #créer un formulaire vide
        return render(request,"shop/paymentForm.html",{'form':form})
    def post(self,request,ido):
        order=Order.objects.get(id=ido)
        form=PaymentForm(request.POST,request.FILES) # récupérer les données saisies dans le formulaire
        if form.is_valid(): # valider les données saisies
            new_costumer=form.save(commit=False)
            new_costumer.costumer_id=order.costumer_id
            new_costumer.save()
            Order.objects.filter(id=ido).update(paid=True)
            messages.success(request,'Thank you for your order, it will be delivered in the briefest delay')
            return  redirect("shop:home")
            
        messages.error(request,'form is not valid')
        return render(request, "shop/paymentForm.html", {'form': form})
        
        

class ProfileView(View):
    def get(self,request):
        if request.user.is_authenticated:
            current_user=request.user
        cart_product_form = CartAddProductForm()
        return render(request,"shop/profile.html",{'current_user':current_user,'cart_product_form':cart_product_form})   

class ProfileUpdateView(View):
    def get(self,request,idp):
        user=User.objects.get(id=idp)
        customer=Costumer.objects.get(user_id=user.id)
        user_form=UserForm(instance=user) #créer un formulaire vide
        costumer_form=CostumerForm(instance=customer) #créer un formulaire vide
        return render(request,"shop/modify_profile.html",{'user_form':user_form,'costumer_form':costumer_form})
        
    def post(self,request,idp):
        user=User.objects.get(id=idp)
        customer=Costumer.objects.get(user_id=user.id)
        user_form=UserForm(request.POST,instance=user)
        costumer_form=CostumerForm(request.POST,request.FILES,instance=customer)
        if user_form.is_valid() and costumer_form.is_valid():
            # Créez un nouvel objet utilisateur mais évitez de l'enregistrer pour le moment
            new_user = user_form.save(commit=False)
            # Définir le mot de passe choisi
            new_user.set_password(user_form.cleaned_data['password'])
            # Enregistrer l'objet Utilisateur
            new_user.is_costumer=True
            new_user.save()
            new_costumer=costumer_form.save(commit=False)
            new_costumer.user=new_user
            # Enregistrer l'objet Client
            new_costumer.save()
            messages.success(request, 'profile modified')
            return redirect("shop:home")
        messages.error(request, 'invalid data')
        return  redirect("shop:profileupdate")

def is_costumer(user):
    if user.is_authenticated and user.is_costumer:
        return True
    return False
@user_passes_test(is_costumer, login_url='/login/')
def cart_add(request, product_id):
    cart = request.session.get(settings.CART_SESSION_ID,{})
    print(request.POST)
    product = Product.objects.get(id=product_id)
    product_id = str(product.id)
    if product_id not in cart:
            cart[product_id] = {'quantity': 1,'price': product.price}

    request.session[settings.CART_SESSION_ID]=cart
    messages.info(request, 'product added')
    return redirect('shop:productList')

def cart_update(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get(settings.CART_SESSION_ID)
    if int(request.POST.get('quantity'))<= int(product.countInStock):
        cart[str(product_id)]['quantity']=request.POST.get('quantity')
        request.session[settings.CART_SESSION_ID]=cart
        messages.success(request, 'quantity modified')
        return redirect('shop:cart_detail')

    messages.error(request, 'not enough stock')
    return redirect('shop:cart_detail')


def cart_remove(request, product_id):
    cart=request.session.get(settings.CART_SESSION_ID)
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session[settings.CART_SESSION_ID]=cart
    return redirect('shop:cart_detail')
def cart_detail(request):
    cart = request.session.get(settings.CART_SESSION_ID,{})
    cart_total_price=0

    for key,val in cart.items():
        product = Product.objects.get(id=key)
        cart[str(product.id)]['product']=product
        cart[str(product.id)]['price'] = product.price
        cart[str(product.id)]['total_price'] = float(cart[str(product.id)]['price']) * float(cart[str(product.id)]['quantity'])
        cart_total_price+=cart[str(product.id)]['total_price']
    
    return render(request, 'shop/cart_detail.html', {'cart': cart,'cart_total_price':cart_total_price})




def order_create(request):
    cart = request.session.get(settings.CART_SESSION_ID)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.costumer=request.user.costumer
            order.save()

            for key,val in cart.items():
                product = Product.objects.get(id=int(key))
                OrderItem.objects.create(order=order,product=product,price=val['price'],quantity=val['quantity'])
            # Vider le panier
            del request.session[settings.CART_SESSION_ID]
            messages.info(request, 'Votre commande a été crée avec succès. Votre numéro de commande est:'+str(order.id))
            return redirect('shop:home')
    else:
        cart_total_price=0
        for key,val in cart.items():
            cart_total_price+= float(cart[key]['price']) * float(cart[key]['quantity'])
        form = OrderCreateForm()
        return render(request,'shop/create_order.html',{'form': form,'cart_total_price':cart_total_price})

class Register(View):
    def get(self,request):
        user_form = UserForm()
        costumer_form = CostumerForm()
        return render(request,'shop/register.html',{'user_form': user_form,'costumer_form':costumer_form})
    def post(self,request):
        user_form = UserForm(request.POST)
        costumer_form = CostumerForm(request.POST,request.FILES)

        if user_form.is_valid() and costumer_form.is_valid():
            # Créez un nouvel objet utilisateur mais évitez de l'enregistrer pour le moment
            new_user = user_form.save(commit=False)
            # Définir le mot de passe choisi
            new_user.set_password(user_form.cleaned_data['password'])
            # Enregistrer l'objet Utilisateur
            new_user.is_costumer=True
            new_user.save()
            new_costumer=costumer_form.save(commit=False)
            new_costumer.user=new_user
            # Enregistrer l'objet Client
            new_costumer.save()
            messages.success(request, 'succesful register')
            return render(request,'shop/register_done.html',{'new_user': new_user})
        messages.error(request, 'invalid data')
        return redirect('shop:register')

class User_login(View):
    def get(self,request):
        form = LoginForm()
        return render(request, 'shop/login.html', {'form': form})
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'succesful login')
                    return redirect('shop:productList')
                else:
                    messages.error(request, 'account disabled')
                    return redirect('shop:login')
                    
            else:
                messages.error(request, 'login or password incorrect')
                return redirect('shop:login')
                
        return redirect("shop:home")

def user_logout(request):
    logout(request)
    messages.success(request, 'logged out')
    return redirect('shop:home')
def rechercher(request):
    products=Product.objects.filter(name__icontains=request.POST.get("cle"))
    return render(request,"shop/product_list.html",{'products':products})