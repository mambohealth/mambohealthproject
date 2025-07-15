import os
import requests
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import json

def get_food_items_from_image(image_data):
    """Identifies food items from an image using the Google Gemini API."""
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        img = Image.open(BytesIO(image_data))
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = "Identify the food items in this image. Please provide a simple, comma-separated list."
        response = model.generate_content([prompt, img])
        
        print(f"Gemini response: {response.text}") # LOGGING
        return response.text.strip()
        
    except Exception as e:
        print(f"Google Gemini API request failed: {e}")
        return ""

def get_food_name_from_image(image_data):
    """Generates a name for the food in an image using the Google Gemini API."""
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        img = Image.open(BytesIO(image_data))
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = "What is the most likely name of the food in this image? Respond with only the food name, without any introductory phrases or markdown."
        response = model.generate_content([prompt, img])
        
        print(f"Gemini name generation response: {response.text}") # LOGGING
        
        # Clean up the response
        name = response.text.strip()
        name = name.replace('*', '') # Remove asterisks
        # Add any other cleaning steps if needed
        
        return name
        
    except Exception as e:
        print(f"Google Gemini API request failed: {e}")
        return ""

def get_nutrition_data(query):
    """Gets nutritional data for a query using the Nutritionix API."""
    print(f"Querying Nutritionix with: {query}")  # LOGGING
    headers = {
        'x-app-id': os.getenv("NUTRITIONIX_APP_ID", "YOUR_APP_ID"),
        'x-app-key': os.getenv("NUTRITIONIX_API_KEY", "YOUR_API_KEY"),
        'Content-Type': 'application/json'
    }
    data = {'query': query}
    try:
        response = requests.post("https://trackapi.nutritionix.com/v2/natural/nutrients", headers=headers, json=data)
        response.raise_for_status()
        nutrition_data = response.json()
        print(f"Nutritionix response: {nutrition_data}")  # LOGGING
        return nutrition_data
    except requests.exceptions.RequestException as e:
        print(f"Nutritionix API request failed: {e}")
        return {}

def extract_nutrition_data(nutrition_data):
    foods = nutrition_data.get('foods', [])
    
    total_calories = sum(food.get('nf_calories') or 0 for food in foods)
    total_protein = sum(food.get('nf_protein') or 0 for food in foods)
    total_carbohydrates = sum(food.get('nf_total_carbohydrate') or 0 for food in foods)
    total_fat = sum(food.get('nf_total_fat') or 0 for food in foods)
    total_saturated_fat = sum(food.get('nf_saturated_fat') or 0 for food in foods)
    total_cholesterol = sum(food.get('nf_cholesterol') or 0 for food in foods)
    total_sodium = sum(food.get('nf_sodium') or 0 for food in foods)
    total_potassium = sum(food.get('nf_potassium') or 0 for food in foods)
    total_fiber = sum(food.get('nf_dietary_fiber') or 0 for food in foods)
    total_sugars = sum(food.get('nf_sugars') or 0 for food in foods)
    
    total_vitamin_c = 0
    total_omega3_epa_dha = 0
    for food in foods:
        if food.get('full_nutrients'):
            for nutrient in food['full_nutrients']:
                # EPA (attr_id: 629) and DHA (attr_id: 621) are in mg
                if nutrient['attr_id'] in [629, 621]:
                    total_omega3_epa_dha += nutrient['value']
                # Vitamin C (attr_id: 401) is in mg
                if nutrient['attr_id'] == 401:
                    total_vitamin_c += nutrient['value']

    return {
        'calories': round(total_calories, 2),
        'protein': round(total_protein, 2),
        'carbohydrates': round(total_carbohydrates, 2),
        'fat': round(total_fat, 2),
        'saturated_fat': round(total_saturated_fat, 2),
        'cholesterol': round(total_cholesterol, 2),
        'sodium': round(total_sodium, 2),
        'potassium': round(total_potassium, 2),
        'fiber': round(total_fiber, 2),
        'sugars': round(total_sugars, 2),
        'vitamin_c': round(total_vitamin_c, 2),
        'omega3_epa_dha': round(total_omega3_epa_dha, 2),
    }

def analyze_meal(image_data=None, name=None, ingredients=None, notes=None):
    """
    Analyzes a meal from an image and/or name and returns nutritional information 
    from both photo analysis and typical data for the name.
    """
    photo_data = {}
    typical_data = {}
    ingredients_data = {}
    generated_name = None

    if image_data:
        image_bytes = image_data.read()
        # Reset buffer to the beginning
        image_data.seek(0)
        
        if not name:
            generated_name = get_food_name_from_image(image_bytes)
            name = generated_name
        
        photo_query = get_food_items_from_image(image_bytes)
        if photo_query:
            photo_nutrition_data = get_nutrition_data(photo_query)
            photo_data = extract_nutrition_data(photo_nutrition_data)
            photo_data['data_source'] = 'PHOTO_ANALYSIS'

    if ingredients:
        ingredients_nutrition_data = get_nutrition_data(ingredients)
        ingredients_data = extract_nutrition_data(ingredients_nutrition_data)
        ingredients_data['data_source'] = 'INGREDIENTS_ANALYSIS'
        return photo_data, ingredients_data, generated_name

    if name:
        typical_nutrition_data = get_nutrition_data(name)
        typical_data = extract_nutrition_data(typical_nutrition_data)
        typical_data['data_source'] = 'TYPICAL_DATA'

    return photo_data, typical_data, generated_name
