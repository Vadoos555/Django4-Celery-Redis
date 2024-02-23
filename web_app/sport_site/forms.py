from typing import Any
from django import forms

from .models import Category, Soulmate, Sport


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Sport
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'soulmate', 'tag']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 20}),
        }
        labels = {'slug': 'URL'}
        
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category',
                                 empty_label='Category not selected')
    soulmate = forms.ModelChoiceField(queryset=Soulmate.objects.all(), required=False,
                                      label='Soulmate', empty_label='unmarried')
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise forms.ValidationError('Length exceeds 50 characters')
        
        return title
    

class UploadFileForm(forms.Form):
    file = forms.FileField(label='File')
