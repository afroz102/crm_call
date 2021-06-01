from django import forms
from home.models import LeadStage
from .models import Lead


class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['stage', 'title', 'contact_person', 'email',
                  'phone', 'designation', 'source']

        widgets = {
            'stage': forms.Select(attrs={
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'title': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'contact_person': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'email': forms.EmailInput(attrs={
                'type': 'email',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'phone': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'designation': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'source': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
        }

    # only stage associated with company will be shown
    def __init__(self, company=None, *args, ** kwargs):
        super(AddLeadForm, self).__init__(*args, **kwargs)
        if company:
            self.fields['stage'].queryset = LeadStage.objects.filter(
                company=company)


# class UpdateLeadForm(forms.ModelForm):
#     class Meta:
#         model = Lead
#         fields = ['title', 'contact_person', 'email',
#                   'phone', 'designation', 'source']
#
#         widgets = {
#             'title': forms.TextInput(attrs={
#                 'type': 'text',
#                 'class': "form-control",
#                 'autofocus': 'autofocus',
#             }),
#             'contact_person': forms.TextInput(attrs={
#                 'type': 'text',
#                 'class': "form-control",
#                 'autofocus': 'autofocus',
#             }),
#             'email': forms.EmailInput(attrs={
#                 'type': 'email',
#                 'class': "form-control",
#                 'autofocus': 'autofocus',
#             }),
#             'phone': forms.TextInput(attrs={
#                 'type': 'text',
#                 'class': "form-control",
#                 'autofocus': 'autofocus',
#             }),
#             'designation': forms.TextInput(attrs={
#                 'type': 'text',
#                 'class': "form-control",
#                 'autofocus': 'autofocus',
#             }),
#             'source': forms.TextInput(attrs={
#                 'type': 'text',
#                 'class': "form-control",
#                 'autofocus': 'autofocus',
#             }),
#         }
#
#     # only stage associated with company will be shown
#     # def __init__(self, company=None, *args, ** kwargs):
#     #     super(AddLeadForm, self).__init__(*args, **kwargs)
#     #     if company:
#     #         self.fields['stage'].queryset = LeadStage.objects.filter(
#     #             company=company)
