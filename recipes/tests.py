import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from .models import Recipe, Category


@pytest.fixture
def user():
    """
    Create a test user
    """
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='password123'
    )


@pytest.fixture
def category(user):
    """
    Create a test category
    """
    return Category.objects.create(
        name="Test Category",
        description="Test category description",
        author=user
    )


@pytest.fixture
def recipe(user, category):
    """
    Create a test recipe
    """
    return Recipe.objects.create(
        title="Test Recipe",
        description="Test recipe description",
        ingredients="Ingredient 1\nIngredient 2",
        instructions="Step 1\nStep 2",
        prep_time=15,
        cook_time=30,
        servings=4,
        category=category,
        author=user
    )


@pytest.mark.django_db
def test_recipe_list_view():
    """
    Test that recipe list view returns 200 status code
    """
    client = Client()
    url = reverse('recipe_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_recipe_creation(user, category):
    """
    Test recipe creation functionality
    """
    # Create a recipe
    recipe = Recipe.objects.create(
        title="Test Recipe",
        description="Test recipe description",
        ingredients="Ingredient 1\nIngredient 2",
        instructions="Step 1\nStep 2",
        prep_time=15,
        cook_time=30,
        servings=4,
        category=category,
        author=user
    )
    
    # Verify that the recipe was created correctly
    assert Recipe.objects.count() == 1
    assert recipe.title == "Test Recipe"
    assert recipe.prep_time == 15
    assert recipe.category.name == "Test Category"
    assert recipe.author.username == "testuser"


@pytest.mark.django_db
def test_recipe_update(recipe):
    """
    Test recipe update functionality
    """
    # Update the recipe
    recipe.title = "Updated Title"
    recipe.prep_time = 20
    recipe.save()
    
    # Refresh from database
    recipe.refresh_from_db()
    
    # Verify the update
    assert recipe.title == "Updated Title"
    assert recipe.prep_time == 20


@pytest.mark.django_db
def test_recipe_delete(recipe):
    """
    Test recipe deletion functionality
    """
    # Verify that the recipe exists
    assert Recipe.objects.count() == 1
    
    # Delete the recipe
    recipe.delete()
    
    # Verify that the recipe was deleted
    assert Recipe.objects.count() == 0


@pytest.mark.django_db
def test_recipe_author_permission(client, user, recipe):
    """
    Test that only the author or admin can edit/delete a recipe
    """
    # Login as the author
    client.login(username='testuser', password='password123')
    
    # Author should be able to access the edit page
    edit_url = reverse('recipe_update', args=[recipe.pk])
    response = client.get(edit_url)
    assert response.status_code == 200
    
    # Create another user
    other_user = User.objects.create_user(
        username='otheruser',
        email='other@example.com',
        password='password123'
    )
    
    # Login as the other user
    client.logout()
    client.login(username='otheruser', password='password123')
    
    # Other user should not be able to edit the recipe
    response = client.get(edit_url)
    assert response.status_code == 403  # Forbidden


@pytest.mark.django_db
def test_user_recipe_list(client, user, recipe):
    """
    Test that a user can see their own recipes
    """
    # Login as the author
    client.login(username='testuser', password='password123')
    
    # Access my recipes page
    url = reverse('my_recipes')
    response = client.get(url)
    assert response.status_code == 200
    
    # The recipe should be in the context
    assert len(response.context['recipes']) == 1
    assert response.context['recipes'][0] == recipe