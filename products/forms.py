from django import forms
from .models import Product, Category, Sale
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','sku','category','description','price','stock','image']
        widgets = {'description': forms.Textarea(attrs={'rows':4})}
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']
        widgets = {'description': forms.Textarea(attrs={'rows':3})}
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['quantity']
    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs); self.product = product
    def clean_quantity(self):
        qty = self.cleaned_data['quantity']
        if self.product and qty > self.product.stock: raise forms.ValidationError(f'Only {self.product.stock} units available.')
        return qty
