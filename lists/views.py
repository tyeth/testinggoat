from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
	#todo: display multiple items in the table
	#todo: support more than one list
	if request.method=='POST':
		Item.objects.create(text=request.POST.get('item_text',''))
		return redirect('/')
	
	return render(request,'home.html')