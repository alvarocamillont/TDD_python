from django import forms


class ItemForm(forms.Form):
    item_text = forms.CharField(
        widget=forms.fields.TextInput(
            attrs={
                'placeholder': 'Digite um item a fazer',
                'class': 'form-control input-lg'
                }
        )
    )
