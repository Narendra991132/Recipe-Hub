from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Recipe, Category
from .forms import RecipeForm, CategoryForm


def home(request):
    """
    View for the home page showing recent recipes
    """
    recent_recipes = Recipe.objects.order_by('-created_at')[:5]
    return render(request, 'recipes/home.html', {'recent_recipes': recent_recipes})


# Recipe Views
def recipe_list(request):
    """
    View for listing all recipes with filtering by category
    """
    category_id = request.GET.get('category')
    if category_id:
        recipes = Recipe.objects.filter(category_id=category_id).order_by('-created_at')
    else:
        recipes = Recipe.objects.all().order_by('-created_at')
    
    categories = Category.objects.all()
    return render(request, 'recipes/recipe_list.html', {
        'recipes': recipes,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })


def recipe_detail(request, pk):
    """
    View for showing recipe details
    """
    recipe = get_object_or_404(Recipe, pk=pk)
    # Check if user is author or admin to show edit/delete buttons
    can_edit = request.user.is_authenticated and (request.user == recipe.author or request.user.is_staff)
    
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'can_edit': can_edit
    })


@login_required
def recipe_create(request):
    """
    View for creating a new recipe
    """
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Recipe created successfully!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    
    # Filter categories to only show the user's categories and any categories by admin
    user_categories = Category.objects.filter(author=request.user)
    admin_categories = Category.objects.filter(author__is_staff=True)
    available_categories = (user_categories | admin_categories).distinct()
    
    form.fields['category'].queryset = available_categories
    
    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'title': 'Create Recipe'
    })


@login_required
def recipe_update(request, pk):
    """
    View for updating an existing recipe
    """
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Check if user is the author or an admin
    if recipe.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to edit this recipe.")
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe updated successfully!')
            return redirect('recipe_detail', pk=pk)
    else:
        form = RecipeForm(instance=recipe)
    
    # Filter categories similar to create view
    user_categories = Category.objects.filter(author=request.user)
    admin_categories = Category.objects.filter(author__is_staff=True)
    available_categories = (user_categories | admin_categories).distinct()
    
    form.fields['category'].queryset = available_categories
    
    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'title': 'Edit Recipe'
    })


@login_required
def recipe_delete(request, pk):
    """
    View for deleting a recipe
    """
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Check if user is the author or an admin
    if recipe.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to delete this recipe.")
    
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully!')
        return redirect('recipe_list')
    
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})


@login_required
def my_recipes(request):
    """
    View for displaying only the user's recipes
    """
    recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'recipes/my_recipes.html', {'recipes': recipes})


# Category Views
def category_list(request):
    """
    View for listing all categories
    """
    categories = Category.objects.all()
    return render(request, 'recipes/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    """
    View for creating a new category
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.author = request.user
            category.save()
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'recipes/category_form.html', {
        'form': form,
        'title': 'Create Category'
    })


@login_required
def category_update(request, pk):
    """
    View for updating an existing category
    """
    category = get_object_or_404(Category, pk=pk)
    
    # Check if user is the author or an admin
    if category.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to edit this category.")
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'recipes/category_form.html', {
        'form': form,
        'title': 'Edit Category'
    })


@login_required
def category_delete(request, pk):
    """
    View for deleting a category
    """
    category = get_object_or_404(Category, pk=pk)
    
    # Check if user is the author or an admin
    if category.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to delete this category.")
    
    if request.method == 'POST':
        if category.recipes.exists():
            messages.error(request, 'Cannot delete category with recipes. Remove recipes first.')
            return redirect('category_list')
        
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    
    return render(request, 'recipes/category_confirm_delete.html', {'category': category})