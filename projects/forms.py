from django.forms import ModelForm
from django import forms
from .models import Project

class ProjectForm(ModelForm):
    featured_image = forms.ImageField(label='Featured image', required=False, widget=forms.FileInput)

    class Meta:
        model = Project
        fields = ['title', 'description', 'featured_image', 'demo_link', 'source_link', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            placeholder = " ".join(name.split('_'))
            field.widget.attrs.update({'class': "input", 'placeholder': f'Add {placeholder}'})
