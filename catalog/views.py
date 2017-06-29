from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db import models
from django.db import models
from django.views.decorators.cache import cache_page

from .models import Product, Category

class ProductListView(generic.ListView): 

	template_name = 'catalog/products.html'
	context_object_name = 'products'
	paginate_by = 9

	def get_queryset(self):
		queryset = Product.objects.all()
		q = self.request.GET.get('q', '')
		if q:
			queryset = queryset.filter(models.Q(name__icontains=q) | models.Q(category__name__icontains=q))
		return queryset

products = ProductListView.as_view()


class CategoryListView(generic.ListView):
	template_name = 'catalog/category.html'
	context_object_name = 'products'
	def get_queryset(self):
		return Product.objects.filter(category__slug=self.kwargs['slug'])

	def get_context_data(self, **kwargs):
		context = super(CategoryListView, self).get_context_data(**kwargs)
		context['current_category'] = get_object_or_404(Category, slug=self.kwargs['slug'])	
		return context

category = CategoryListView.as_view()

#def category(request, slug):
#	category = Category.objects.get(slug=slug)
#	context = {
#		'current_category': category,
#		'products': Product.objects.filter(category=category),
#	}
#	return render(request, 'catalog/category.html', context)

def product_detail(request, slug):
	product = Product.objects.get(slug=slug)
	context = {
		'product': product
	}
	return render(request, 'catalog/product_detail.html', context)