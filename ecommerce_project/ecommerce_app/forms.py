from django import forms


# Form to add (insert + update) items in Item table.
class ItemForm(forms.Form):
    item_name = forms.CharField(label='Item Name', max_length=30)
    no_of_items = forms.IntegerField(label='Number of Items')


# Form to place single orders in Order table.
class OrderForm(forms.Form):
    item_name = forms.CharField(label='Item name', max_length=50)
    quantity = forms.IntegerField(label='Quantity')
    email_id = forms.EmailField(label='Email id')


