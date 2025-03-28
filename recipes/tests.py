import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from .models import Recipe, Category

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
def test_recipe_create_view():
    """
    Test that recipe create view requires login
    """
    client = Client()
    url = reverse('recipe_create')
    response = client.get(url)
    assert response.status_code == 302  # Should redirect to login


@pytest.mark.django_db
def test_basic_recipe_creation():
    """
    Test basic recipe creation
    """
    # Create a user manually
    user = User.objects.create_user(
        username='testuser123',
        email='testuser123@example.com',
        password='testpassword123'
    )
    
    # Create a category
    category = Category.objects.create(
        name="Test Category",
        description="Test description",
        author=user
    )
    
    # Create a recipe
    recipe = Recipe.objects.create(
        title="Test Recipe",
        description="Test description",
        ingredients="Test ingredients",
        instructions="Test instructions",
        prep_time=30,
        cook_time=60,
        servings=4,
        category=category,
        author=user
    )
    
    # Verify recipe was created
    assert Recipe.objects.filter(title="Test Recipe").exists()
    assert recipe.author == user


@pytest.mark.django_db
def test_category_listing():
    """
    Test category list view
    """
    client = Client()
    url = reverse('category_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_authenticated_views():
    """
    Test views that require authentication
    """
    # Create a user and authenticate
    username = 'loginuser'
    password = 'password123'
    User.objects.create_user(username=username, password=password)
    
    client = Client()
    client.login(username=username, password=password)
    
    # Test authenticated page access
    response = client.get(reverse('profile'))
    assert response.status_code == 200
    
    response = client.get(reverse('my_recipes'))
    assert response.status_code == 200