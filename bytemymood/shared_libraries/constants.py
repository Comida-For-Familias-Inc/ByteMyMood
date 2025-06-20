"""Constants used throughout the ByteMyMood project."""

# System state constants
SYSTEM_TIME = "system_time"
RECIPE_INITIALIZED = "recipe_initialized"

# Recipe state constants
RECIPE_KEY = "recipe"
CURRENT_RECIPE = "current_recipe"
PREP_TIME = "prep_time"
COOK_TIME = "cook_time"
DIFFICULTY = "difficulty"
SERVINGS = "servings"
VERIFICATION_STATUS = "verification_status"
IS_VERIFIED = "is_verified"

# Recipe attributes
INGREDIENTS = "ingredients"
INSTRUCTIONS = "instructions"
CUISINE = "cuisine"
DIETARY_RESTRICTIONS = "dietary_restrictions"
COOKING_METHOD = "cooking_method"
EQUIPMENT = "equipment"
NUTRITIONAL_INFO = "nutritional_info"
SOURCE_URL = "source_url"

# User preferences
USER_PREFERENCES = "user_preferences"
ALLERGIES = "allergies"
DIETARY_PREFERENCES = "dietary_preferences"
COOKING_SKILL_LEVEL = "cooking_skill_level"
EQUIPMENT_AVAILABLE = "equipment_available"
TIME_CONSTRAINTS = "time_constraints"

# State keys
MEAL_PLAN_INITIALIZED = "meal_plan_initialized"
MEAL_PLAN_KEY = "meal_plan"
MEAL_PLAN_START_DATE = "meal_plan_start_date"
MEAL_PLAN_END_DATE = "meal_plan_end_date"
MEAL_PLAN_DATETIME = "meal_plan_datetime"

# Meal plan keys
START_DATE = "start_date"
END_DATE = "end_date"

# User profile keys
USER_PROFILE = "user_profile"
PREFERENCES = "preferences"
KITCHEN_EQUIPMENT = "kitchen_equipment"
MEAL_PREFERENCES = "meal_preferences"

# Recipe keys
RECIPE_NAME = "name"
RECIPE_DESCRIPTION = "description"
RECIPE_NUTRITION = "nutrition"

# Meal slot keys
MEAL_TYPE = "meal_type"
MEAL_TIME = "meal_time"
MEAL_RECIPE = "recipe"
MEAL_NOTES = "notes"

# Nutrition keys
CALORIES = "calories"
PROTEIN = "protein"
CARBS = "carbs"
FAT = "fat"
FIBER = "fiber"
SUGAR = "sugar"
SODIUM = "sodium"

# Shopping list keys
INGREDIENT_NAME = "name"
INGREDIENT_AMOUNT = "amount"
INGREDIENT_UNIT = "unit"
INGREDIENT_CATEGORY = "category"
INGREDIENT_NOTES = "notes"

# Cooking instruction keys
STEP_NUMBER = "step_number"
STEP_DESCRIPTION = "description"
STEP_TIME = "time"
STEP_TIPS = "tips"

# Image generation state keys
UPLOADED_IMAGE_B64 = "uploaded_image_b64"
UPLOADED_MASK_B64 = "uploaded_mask_b64"
UPLOADED_IMAGE_PARTS = "uploaded_image_parts" 

# --- Image Saving Settings ---
SAVE_IMAGES_LOCALLY: bool = True # Set to False to disable local saving
LOCAL_IMAGE_SAVE_PATH: str = "local_image_results" # Directory relative to project root
