from django import forms
from. models import Category

class CategoryForm(forms.ModelForm):
    cat_image = forms.ImageField(required=True,error_messages = {'Invalid':{"Image files only"}},widget=forms.FileInput)
    class Meta:
        model = Category
        fields = ['category_name','slug','desccription','cat_image']
        
        def __init__(self, *args, **kwargs):
            super(CategoryForm,self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control' 