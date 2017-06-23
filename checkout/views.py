# encoder=utf-8
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory
from django.views.generic import RedirectView, TemplateView
from catalog.models import Product
from .models import CartItem
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

class CreateCartItemView(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		product = get_object_or_404(Product, slug=self.kwargs['slug'])
		if self.request.session.session_key is None:
			self.request.session.save()
		cart_item, created = CartItem.objects.add_item(self.request.session.session_key, product)
		#if created:
		#	messages.success(self.request, 'Produto adicionado com sucesso')
		#else:
		#	messages.success(self.request, 'Produto atualizados com sucesso')
		return reverse('checkout:cart_item')
create_cartitem = CreateCartItemView.as_view()

class CartItemView(TemplateView):
	template_name = 'checkout/chart.html'

	def get_formset(self, clear=False):
		CartItemFormSet = modelformset_factory(CartItem, fields=('quantity',), can_delete=True, extra=0)
		session_key = self.request.session.session_key
		if session_key:
			if clear:
				formset = CartItemFormSet(queryset=CartItem.objects.filter(cart_key=session_key))
			else:
				formset = CartItemFormSet(queryset=CartItem.objects.filter(cart_key=session_key), data=self.request.POST or None)
		else: 
			formset = CartItemFormSet(queryset=CartItem.objects.none())
		return formset	

	def get_context_data(self, **kwargs):
		context = super(CartItemView, self).get_context_data(**kwargs)
		context['formset'] = self.get_formset()
		return context
	def post(self, request, *args, **kwargs):
		formset = self.get_formset()
		context = self.get_context_data(**kwargs)
		if formset.is_valid():
			formset.save()
			context['formset'] = self.get_formset(clear=True)
		return self.render_to_response(context)

cart_item = CartItemView.as_view()


class CheckoutView(LoginRequiredMixin, TemplateView):
	templte_name = 'checkout/checkout.html'
	def get(self, request, *args, **kwargs):
		session_key = request.session.session_key
		if session_key and CartItem.objects.filter(cart_key=session_key).exists():
			cart_items = CartItem.objects.filter(cart_key=session_key)
			order = order.objects.create_order(user=requets.user, cart_items=cart_items)
		else:
			return redirect('checkout:cart_item')
		return super(CheckoutView, self).get(request, *args, **kwargs)
		
checkout = CheckoutView.as_view()