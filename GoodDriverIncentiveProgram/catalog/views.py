from ebaysdk.finding import Connection as finding
from bs4 import BeautifulSoup
from ebaysdk.finding import Connection as Finding
from django.urls import reverse, reverse_lazy, path
from django.conf.urls import url
from django.contrib import messages
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from catalog.models import Item, OrderItem, Order, KeyWord
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.template.defaultfilters import slugify
from django.core.mail import send_mail
import random
from requests.exceptions import ConnectionError

ITEM_INFO_COUNT = 4
CATALOG_ITEM_WIDTH = 4
ID_APP = 'AlexHaig-CPSC4140-PRD-369ec6afc-bad2a087'
MAX_ENTRIES = 50
NO_IMAGE = 'https://thumbs1.ebaystatic.com/pict/04040_0.jpg'

def addCatalog(word, keyWord, request):
    api = Finding(appid=ID_APP, config_file=None, https=True)
    response = api.execute('findItemsAdvanced', {'keywords': word, 'paginationInput': [{'entriesPerPage': MAX_ENTRIES}]})
    products = response.dict()
    products = products["searchResult"]
    i = 0

    for product in products["item"]:
        slug = slugify(product["title"])
        num = random.randint(1, 10000)
        slug += str(num)
        try:
            Item.objects.create(title=product["title"], price=float(product["sellingStatus"]["convertedCurrentPrice"]["value"]), imgUrl=product["galleryURL"], condition=product["condition"]["conditionDisplayName"], conditionId=product["condition"]["conditionId"], slug=slug, keyWord=keyWord)
        except:
            Item.objects.create(title=product["title"], price=float(product["sellingStatus"]["convertedCurrentPrice"]["value"]), imgUrl=NO_IMAGE, condition='', conditionId=0, slug=slug, keyWord=keyWord)


def getAllKeyWords():
    allWordsOdj = KeyWord.objects.all()
    allwords = []
    for word in allWordsOdj:
        allwords.append(word)
    return allwords

def deleteWords(request):
    if request.method == 'POST':
        KeyWord.objects.filter(pk=request.POST.get('pk')).delete()
        messages.info(request, "Word removed from keyword list")
    return render(request, 'deleteWords.html', {'allWords':getAllKeyWords()})

def catalog(request):
    allItems = []
    for i in range(0, MAX_ENTRIES):
        for j in range(0, KeyWord.objects.all().count()):
            allItems.append(Item.objects.all()[(j*MAX_ENTRIES)+i])
    return render(request, 'catalog.html', {'allItems': allItems})

def addWords(request):
    if request.method == 'POST':
        word = request.POST.get('addWords')
        if word != None:
            try:
                Finding(appid=ID_APP, config_file=None, https=True).execute('findItemsAdvanced', {'keywords': word, 'paginationInput': [{'entriesPerPage': MAX_ENTRIES}]})
            except ConnectionError as e:
                messages.info(request, "Unable to add word to keyword list")
                return render(request, 'addwords.html', {'keyWords': KeyWord.objects.all()})
            keyWord = KeyWord.objects.create(word=word)
            addCatalog(word, keyWord, request)
            message = word + " was added to keyword list"
            messages.info(request, message)
    try:
        return render(request, 'addwords.html', {'keyWords': KeyWord.objects.all()})
    except:
        return render(request, 'addwords.html', {'keyWords': []})

def checkoutPage(request):
    items = Order.objects.filter(user=request.user, ordered=False)
    sum = 0
    len = 0
    checkout = True
    if items.exists():
        for item in items[0].items.all():
            sum += item.item.price*item.quantity
            len += 1*item.quantity
        items = items[0].items.all()
    else:
        items = {}
        checkout = False
    return render(request, 'checkout-page.html', {'checkout': checkout, 'items': items, 'len': len, 'sum': sum, 'blank':''})

def prodDetail(request, slug):
    item = Item.objects.filter(slug=slug)
    return render(request, 'product-page.html', {'item': item[0]})

def addToCart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    orderItem, created = OrderItem.objects.get_or_create(item=item, user = request.user, ordered=False)
    orderSet = Order.objects.filter(user=request.user, ordered=False)
    if orderSet.exists():
        order = orderSet[0]
        if order.items.filter(item__slug=item.slug).exists():
            orderItem.quantity += 1
            orderItem.save()
            messages.info(request, "Item quantity updated")
            return redirect("catalog:checkoutPage")
        else:
            messages.info(request, "Item added to cart")
            order.items.add(orderItem)
            return redirect("catalog:checkoutPage")
    else:
        order = Order.objects.create(user=request.user, orderDate=timezone.now())
        order.items.add(orderItem)
        messages.info(request, "Item added to cart")
        return redirect("catalog:checkoutPage")

def remFromCart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    orderSet = Order.objects.filter(user=request.user, ordered=False)
    if orderSet.exists():
        order = orderSet[0]
        if order.items.filter(item__slug=item.slug).exists():
            orderItem = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if orderItem.quantity > 1:
                orderItem.quantity -= 1
                orderItem.save()
                messages.info(request, "Item quantity updated")
                return redirect("catalog:checkoutPage")
            else:
                orderItem.quantity -= 1
                order.items.remove(orderItem)
                orderItem.delete()
                messages.info(request, "Item removed from cart")
                return redirect("catalog:checkoutPage")
        else:
            messages.info(request, "Item not in cart")
            return redirect("catalog:checkoutPage")
    else:
        messages.info(request, "No valid active order")
        return redirect("catalog:checkoutPage")

def checkout(request):
    firstName = request.GET.get('firstName')
    lastName = request.GET.get('lastName')
    email = request.GET.get('email')
    address = request.GET.get('address')
    address2 = request.GET.get('address2')
    country = request.GET.get('country')
    state = request.GET.get('state')
    zipCode = request.GET.get('zipCode')
    sum = 0
    itemStr ='Thank you for your purchase, ' + firstName + '\n\n'
    itemStr = itemStr + firstName + ' ' + lastName + '\n'
    itemStr = itemStr + address + '\n'
    if address2 != '':
        itemStr = itemStr + address2 + '\n'
    itemStr = itemStr + state + ', ' + country + '\n'
    itemStr = itemStr + zipCode + '\n' + '\n'
    items = Order.objects.filter(user=request.user, ordered=False)
    for item in items[0].items.all():
        sum += item.item.price*item.quantity
        itemStr += item.item.title + '\t'
        itemStr += str(item.item.price)
        itemStr += '\n'
    
    itemStr = itemStr + "\nTotal Cost: " + str(sum)

    send_mail(
        'GDIP: Purchase Confirmation Email',
        itemStr,
        'gdipteam@gmail.com',
        [email],
    )

    order = Order.objects.filter(user=request.user, ordered=False)[0]
    order.ordered = True
    order.save()
    for item in order.items.all():
        print(item.item.title)
        item.ordered = True
        item.save()
    return redirect("catalog:catalog")

def pastOrders(request):
    allOrders = Order.objects.filter(user=request.user, ordered=True)
    return render(request, 'past-orders.html', {'allOrders':allOrders})

def changeShipping(request, pk):
    return render(request, 'new-shipping.html', {'pk':pk})

def processNewShipping(request):
    pk=request.GET.get('pk')
    firstName = request.GET.get('firstName')
    lastName = request.GET.get('lastName')
    email = request.GET.get('email')
    address = request.GET.get('address')
    address2 = request.GET.get('address2')
    country = request.GET.get('country')
    state = request.GET.get('state')
    zipCode = request.GET.get('zipCode')
    sum = 0
    itemStr ='Hi, ' + firstName + '\n' + 'Your shipping address for order #' + str(pk) + ' has been updated.\nYou can find the new shipping details below.\n\n'
    itemStr = itemStr + firstName + ' ' + lastName + '\n'
    itemStr = itemStr + address + '\n'
    if address2 != '':
        itemStr = itemStr + address2 + '\n'
    itemStr = itemStr + state + ', ' + country + '\n'
    itemStr = itemStr + zipCode + '\n' + '\n'

    subj = 'Order #' + str(pk) + ' Shipping Address Change'
    send_mail(
        subj,
        itemStr,
        'gdipteam@gmail.com',
        [email],
    )


    messages.info(request, "Shipping address successfully changed")
    return redirect("catalog:pastOrders")

def cancelOrder(request, pk):
    sum = 0
    order = Order.objects.filter(user=request.user, pk=pk, ordered=True)[0]
    itemStr ='Hi, ' + request.user.username + '\n\n' + 'You cancelled your order #' + str(pk) + '.\nPlease find the details of your refund below.\n\n'
    for item in order.items.all():
        itemStr+= item.item.title + '\t' + str(item.quantity) + '\n'
        sum += item.item.price*item.quantity


    itemStr += '\nTotal Refund: ' + str(sum)

    subj = 'Order #' + str(pk) + ' Cancellation'
    send_mail(
        subj,
        itemStr,
        'gdipteam@gmail.com',
        [request.user.email],
    )
    order.delete()
    message = 'Order ' + str(pk + ' successfully cancelled')
    messages.info(request, message)
    return redirect("catalog:pastOrders")

