# from leads.models import Lead, LeadStage
# from django import forms
#
#
# class AddLeadForm(forms.ModelForm):
#     class Meta:
#         model = LeadStage
#         fields = ['stage_label']
#
#         widgets = {
#             'stage': forms.Select(attrs={
#                 'class': "form-control",
#                 'autofocus': 'autofocus',
#             }),
#         }
#
#     # only Unit associated with company will be shown
#     def __init__(self, company=None, *args, ** kwargs):
#         super(AddLeadForm, self).__init__(*args, **kwargs)
#         if company:
#             self.fields['stage'].queryset = LeadStage.objects.filter(
#                 company=company)
