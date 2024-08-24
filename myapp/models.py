from django.db import models
from django.core.validators import MinValueValidator

class Products(models.Model):
    ITEM_UNIT = [
        ('number', 'Number'),
        ('litre', 'Litre'),
        ('mm', 'Millimeter (mm)'),
        ('cm', 'Centimeter (cm)'),
        ('in', 'Inch (in)'),
        ('ft', 'Foot (ft)'),
        ('mm2', 'Square Millimeter (mm²)'),
        ('cm2', 'Square Centimeter (cm²)'),
        ('m2', 'Square Meter (m²)'),
        ('ft2', 'Square Foot (ft²)'),
    ]

    item_details = models.CharField(
        max_length=200,
        help_text="name or description of the product",
        null=True
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="quantity of the product"
    )
    unit = models.CharField(
        max_length=20,
        choices=ITEM_UNIT,
        help_text="unit of measurement"
    )
    rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0,
        help_text="rate for each"
    )
    expenses = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="amount used"
    )
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0,
        help_text="previous balance"
    )

    def amount(self):
        self.amount = self.rate * self.quantity
        return self.amount

    
    def save(self,*args,**kwargs):
        amount = self.rate * self.quantity
        if self.pk is None:
            lastRecord = Products.objects.order_by('-id').first()
            if lastRecord:
                self.balance = lastRecord.balance + amount - self.expenses
            else:
                self.balance = amount - self.expenses
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.item_details} - {self.quantity} {self.unit} at {self.rate}/unit"
