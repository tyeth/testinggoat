from django.shortcuts import render
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
	#todo: stop saving an empty item each page load
	#todo: display multiple items in the table
	#todo: support more than one list
	if request.method=='POST':
		new_item_text = request.POST.get('item_text','')
		Item.objects.create(text=new_item_text)
	else:
		new_item_text=''
	
	return render(request,'home.html', {
		'new_item_text': new_item_text, 
		})