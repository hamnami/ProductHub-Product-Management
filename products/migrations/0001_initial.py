from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
class Migration(migrations.Migration):
    initial=True
    dependencies=[]
    operations=[
      migrations.CreateModel(name='Category',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('name',models.CharField(max_length=100,unique=True)),('description',models.TextField(blank=True)),('created_at',models.DateTimeField(auto_now_add=True))]),
      migrations.CreateModel(name='Product',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('name',models.CharField(max_length=150)),('sku',models.CharField(max_length=50,unique=True)),('description',models.TextField(blank=True)),('price',models.DecimalField(decimal_places=2,max_digits=10,validators=[django.core.validators.MinValueValidator(0)])),('stock',models.PositiveIntegerField(default=0)),('image',models.ImageField(blank=True,null=True,upload_to='products/')),('created_at',models.DateTimeField(auto_now_add=True)),('updated_at',models.DateTimeField(auto_now=True)),('category',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name='products',to='products.category'))]),
      migrations.CreateModel(name='Sale',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('quantity',models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),('unit_price',models.DecimalField(decimal_places=2,max_digits=10)),('sold_at',models.DateTimeField(auto_now_add=True)),('product',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='sales',to='products.product'))])
    ]
