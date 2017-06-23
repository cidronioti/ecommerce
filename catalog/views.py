from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Product, Category

class ProductListView(generic.ListView): 
	model = Product
	template_name = 'catalog/products.html'
	context_object_name = 'products'
	paginate_by = 9

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