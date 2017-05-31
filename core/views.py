# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
	return render(request, 'index.html')

def contact(request):
	return render(request, 'contact.html')

def product_detail(request):
	return render(request, 'product_detail.html')

def products(request):
	return render(request, 'products.html')

def chart(request):
	return render(request, 'chart.html')

def login(request):
	return render(request, 'login.html')

def checkout(request):
	return render(request, 'checkout.html')