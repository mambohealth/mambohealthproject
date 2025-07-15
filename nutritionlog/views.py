from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import NutritionLog, Food
from .forms import NutritionLogForm, FoodForm
from .nutrition_analysis import analyze_meal, get_nutrition_data, extract_nutrition_data
import base64
from datetime import date

@login_required
def food_list(request):
    foods = Food.objects.filter(user=request.user)
    return render(request, 'nutritionlog/food_list.html', {'foods': foods})

@login_required
def create_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            food.user = request.user
            food.save()
            return redirect('food_list')
    else:
        form = FoodForm()
    return render(request, 'nutritionlog/food_form.html', {'form': form})

@login_required
def edit_food(request, food_id):
    food = get_object_or_404(Food, id=food_id, user=request.user)
    if request.method == 'POST':
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return redirect('food_list')
    else:
        form = FoodForm(instance=food)
    return render(request, 'nutritionlog/food_form.html', {'form': form})

@login_required
def delete_food(request, food_id):
    food = get_object_or_404(Food, id=food_id, user=request.user)
    if request.method == 'POST':
        food.delete()
        return redirect('food_list')
    return render(request, 'nutritionlog/food_confirm_delete.html', {'food': food})

@login_required
def nutritionlog_list(request):
    if request.method == 'POST':
        form = NutritionLogForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            saved_food = form.cleaned_data.get('saved_food')
            if saved_food:
                log = NutritionLog(
                    user=request.user,
                    date=form.cleaned_data['date'],
                    meal_type=form.cleaned_data['meal_type'],
                    name=saved_food.name,
                    calories=saved_food.calories,
                    protein=saved_food.protein,
                    carbohydrates=saved_food.carbohydrates,
                    fat=saved_food.fat,
                    saturated_fat=saved_food.saturated_fat,
                    cholesterol=saved_food.cholesterol,
                    sodium=saved_food.sodium,
                    potassium=saved_food.potassium,
                    fiber=saved_food.fiber,
                    sugars=saved_food.sugars,
                    vitamin_c=saved_food.vitamin_c,
                    omega3_epa_dha=saved_food.omega3_epa_dha,
                    data_source='USER_INPUT'
                )
                log.save()
                return redirect('nutritionlog_list')

            meal_photo = request.FILES.get('meal_photo')
            name = form.cleaned_data.get('name')
            ingredients = form.cleaned_data.get('ingredients')
            
            if meal_photo or ingredients:
                photo_data, typical_data, generated_name = analyze_meal(
                    image_data=meal_photo, 
                    name=name, 
                    ingredients=ingredients
                )
                
                # Store data in session to pass to the confirmation view
                form_data = form.cleaned_data
                form_data['date'] = form_data['date'].isoformat() # Convert date to string
                if 'meal_photo' in form_data:
                    del form_data['meal_photo'] # remove non-serializable object
                if 'saved_food' in form_data:
                    del form_data['saved_food']
                request.session['nutrition_form_data'] = form_data

                if meal_photo:
                    # Encode photo to store in session
                    meal_photo.seek(0)
                    request.session['meal_photo'] = base64.b64encode(meal_photo.read()).decode('utf-8')
                
                request.session['photo_nutrition_data'] = photo_data
                request.session['typical_nutrition_data'] = typical_data
                if generated_name:
                    request.session['nutrition_form_data']['name'] = generated_name

                return redirect('nutritionlog_confirm')

            # If no photo or ingredients, save directly
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('nutritionlog_list')
    else:
        form = NutritionLogForm(user=request.user)
    
    log_list = NutritionLog.objects.filter(user=request.user)
    paginator = Paginator(log_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, 'nutritionlog/nutritionlog_list.html', context)

@login_required
def nutritionlog_confirm(request):
    context = {
        'photo_data': request.session.get('photo_nutrition_data'),
        'typical_data': request.session.get('typical_nutrition_data'),
        'form_data': request.session.get('nutrition_form_data'),
    }
    return render(request, 'nutritionlog/nutritionlog_confirm.html', context)

@login_required
def update_nutrition_name(request):
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        if new_name:
            # Update the name in the session
            form_data = request.session.get('nutrition_form_data', {})
            form_data['name'] = new_name
            request.session['nutrition_form_data'] = form_data

            # Get new typical nutrition data
            typical_nutrition_data = get_nutrition_data(new_name)
            typical_data = extract_nutrition_data(typical_nutrition_data)
            typical_data['data_source'] = 'TYPICAL_DATA'
            request.session['typical_nutrition_data'] = typical_data

    return redirect('nutritionlog_confirm')


@login_required
def save_nutrition_log(request):
    if request.method == 'POST':
        source = request.POST.get('source')
        form_data = request.session.get('nutrition_form_data')
        
        if source == 'photo':
            nutrition_data = request.session.get('photo_nutrition_data')
        else:
            nutrition_data = request.session.get('typical_nutrition_data')

        log = NutritionLog(
            user=request.user,
            date=date.fromisoformat(form_data['date']), # Convert string back to date
            meal_type=form_data['meal_type'],
            name=form_data.get('name'),
            ingredients=form_data.get('ingredients'),
            notes=form_data.get('notes'),
            calories=nutrition_data.get('calories'),
            protein=nutrition_data.get('protein'),
            carbohydrates=nutrition_data.get('carbohydrates'),
            fat=nutrition_data.get('fat'),
            saturated_fat=nutrition_data.get('saturated_fat'),
            cholesterol=nutrition_data.get('cholesterol'),
            sodium=nutrition_data.get('sodium'),
            potassium=nutrition_data.get('potassium'),
            fiber=nutrition_data.get('fiber'),
            sugars=nutrition_data.get('sugars'),
            vitamin_c=nutrition_data.get('vitamin_c'),
            omega3_epa_dha=nutrition_data.get('omega3_epa_dha'),
            data_source=nutrition_data.get('data_source')
        )
        
        if 'meal_photo' in request.session:
            from django.core.files.base import ContentFile
            log.meal_photo.save(f"{form_data.get('name', 'meal')}.jpg", ContentFile(base64.b64decode(request.session['meal_photo'])))

        log.save()

        # Clean up session
        del request.session['nutrition_form_data']
        del request.session['photo_nutrition_data']
        del request.session['typical_nutrition_data']
        if 'meal_photo' in request.session:
            del request.session['meal_photo']

        return redirect('nutritionlog_list')
    
    return redirect('nutritionlog_list')

@login_required
def edit_nutrition_log(request, log_id):
    log = get_object_or_404(NutritionLog, id=log_id, user=request.user)
    if request.method == 'POST':
        form = NutritionLogForm(request.POST, request.FILES, instance=log, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('nutritionlog_list')
    else:
        form = NutritionLogForm(instance=log, user=request.user)
    return render(request, 'nutritionlog/nutritionlog_edit_form.html', {'form': form})

@login_required
def delete_nutrition_log(request, log_id):
    log = get_object_or_404(NutritionLog, id=log_id, user=request.user)
    if request.method == 'POST':
        log.delete()
        return redirect('nutritionlog_list')
    return render(request, 'nutritionlog/nutritionlog_confirm_delete.html', {'log': log})
