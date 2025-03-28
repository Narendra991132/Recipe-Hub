from django import forms
from .models import Recipe, Category


class CategoryForm(forms.ModelForm):
    """
    Form for creating and updating categories
    """
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class RecipeForm(forms.ModelForm):
    """
    Form for creating and updating recipes
    """
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 
                  'prep_time', 'cook_time', 'servings', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'prep_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'cook_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'servings': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }