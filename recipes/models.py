from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Model for recipe categories
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories", null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Recipe(models.Model):
    """
    Model for storing recipe information
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    prep_time = models.IntegerField(help_text="Preparation time in minutes")
    cook_time = models.IntegerField(help_text="Cooking time in minutes")
    servings = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recipes")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title