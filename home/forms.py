from home.models import CustomField
from django import forms


class AddCustomFieldForm(forms.ModelForm):
    class Meta:
        model = CustomField
        fields = ['field_title', 'field_type']

        widgets = {
            'field_title': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
            }),
            'field_type': forms.Select(attrs={
                'class': "form-control",
            }),
        }
