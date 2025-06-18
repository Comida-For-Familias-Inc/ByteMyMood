"""Common data schema and types for meal-planning-assistant agents."""

from typing import List, Optional, Dict, Any

from google.genai import types
from pydantic import BaseModel, Field


# Convenient declaration for controlled generation
json_response_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)


class UserProfile(BaseModel):
    """User profile information."""
    dietary_restrictions: List[str] = Field(default_factory=list, description="List of dietary restrictions")
    allergies: List[str] = Field(default_factory=list, description="List of food allergies")
    preferences: List[str] = Field(default_factory=list, description="List of food preferences")
    cooking_skill_level: str = Field(..., description="User's cooking skill level (beginner, intermediate, advanced)")
    kitchen_equipment: List[str] = Field(default_factory=list, description="Available kitchen equipment")
    meal_preferences: Dict[str, Any] = Field(default_factory=dict, description="Preferences for different meal types")


class Ingredient(BaseModel):
    """An ingredient in a recipe."""
    name: str = Field(..., description="Name of the ingredient")
    quantity: str = Field(..., description="Quantity of the ingredient")
    unit: str = Field(..., description="Unit of measurement")
    category: str = Field(..., description="Category of ingredient (e.g., produce, dairy, meat)")


class Recipe(BaseModel):
    """A recipe for a meal."""
    name: str = Field(..., description="Name of the recipe")
    cuisine: str = Field(..., description="Type of cuisine")
    prep_time_minutes: int = Field(..., description="Preparation time in minutes")
    cook_time_minutes: int = Field(..., description="Cooking time in minutes")
    servings: int = Field(..., description="Number of servings")
    calories_per_serving: int = Field(..., description="Calories per serving")
    ingredients: List[Ingredient] = Field(..., description="List of ingredients")
    instructions: List[str] = Field(..., description="Step-by-step cooking instructions")
    dietary_tags: List[str] = Field(..., description="List of dietary tags (e.g., vegetarian, gluten-free)")
    image_url: Optional[str] = Field(None, description="URL to recipe image")


class MealSlot(BaseModel):
    """A single meal slot in the plan."""
    meal_type: str = Field(..., description="Type of meal (breakfast, lunch, dinner)")
    time: str = Field(..., description="Scheduled time for the meal")
    duration_minutes: int = Field(..., description="Expected duration of meal preparation")
    recipe: Optional[Recipe] = Field(None, description="Selected recipe for this meal")
    notes: Optional[str] = Field(None, description="Additional notes for the meal slot")


class DailyMealPlan(BaseModel):
    """A single day's meal plan."""
    date: str = Field(..., description="Date of the meal plan")
    meals: List[MealSlot] = Field(..., description="List of meals for the day")
    total_calories: int = Field(..., description="Total calories for the day")
    cuisine_theme: Optional[str] = Field(None, description="Theme for the day's meals")


class MacroTargets(BaseModel):
    """Macronutrient targets for a meal plan."""
    calories_per_day: int = Field(..., description="Target calories per day")
    protein_grams: int = Field(..., description="Target protein in grams")
    carbs_grams: int = Field(..., description="Target carbohydrates in grams")
    fat_grams: int = Field(..., description="Target fat in grams")
    meal_distribution: Dict[str, float] = Field(..., description="Distribution of calories across meals")


class NutritionReport(BaseModel):
    """Nutritional analysis of a meal plan."""
    daily_averages: Dict[str, float] = Field(..., description="Average daily nutritional values")
    meal_distribution: Dict[str, Dict[str, float]] = Field(..., description="Nutritional values per meal type")
    recommendations: List[str] = Field(..., description="Nutritional recommendations")


class ShoppingList(BaseModel):
    """Shopping list for the meal plan."""
    ingredients: List[Dict[str, Any]] = Field(..., description="List of ingredients to purchase")
    categories: Dict[str, List[str]] = Field(..., description="Ingredients grouped by category")
    total_items: int = Field(..., description="Total number of unique items")
    estimated_cost: Optional[float] = Field(None, description="Estimated total cost")


class CookingInstructions(BaseModel):
    """Step-by-step cooking instructions."""
    daily_instructions: Dict[str, List[Dict[str, Any]]] = Field(..., description="Instructions organized by day")
    parallel_tasks: List[Dict[str, Any]] = Field(..., description="Tasks that can be done in parallel")
    prep_ahead: List[Dict[str, Any]] = Field(..., description="Tasks that can be prepared ahead") 