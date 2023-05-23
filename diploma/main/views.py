from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from .forms import PredictionForm, RegistrationForm, LoginForm
from .models import History
from .data import Building_and_Condition_Types
from .predictor import myModel

from collections import Counter


# MAIN PAGE
def index(request):

    if request.method == "POST":
        prediction_form = PredictionForm(request.POST)
        toShow = False
    
        if prediction_form.is_valid():
            
            # FORM DATA
            total_area = prediction_form.cleaned_data['total_area']
            number_of_levels = prediction_form.cleaned_data['number_of_levels']
            buildingType = prediction_form.cleaned_data['buildingType']
            condition = prediction_form.cleaned_data['condition']
            ceilings = prediction_form.cleaned_data['ceilings']
            parking = prediction_form.cleaned_data['parking']
            firealarm = prediction_form.cleaned_data['firealarm']
            security = prediction_form.cleaned_data['security']
            video_surveillance = prediction_form.cleaned_data['video_surveillance']
            alarm_system = prediction_form.cleaned_data['alarm_system']
            optics = prediction_form.cleaned_data['optics']

            # PREIDICTION
            prediction = myModel.predict(myModel, total_area, number_of_levels, buildingType, condition, ceilings, parking, firealarm, security, video_surveillance, alarm_system, optics)
            
            # PROPERTIES WITH SIMILAR PRICE ON KRYSHA
            toShow = True
            property_on_krysha_with_similar_price = f"https://krisha.kz/prodazha/pomeshhenija/?das[price][from]={int(prediction * 0.95)}&das[price][to]={int(prediction * 1.05)}"

            # CHECKING IF USER IS LOGGED IN
            form_user = None
            if not request.user.is_anonymous:
                form_user = User.objects.get(username=request.user)
            
            # INSERTING DATA FORM TO THE DATABSE (ONLY IF USER IS LOGGED IN)
            History.objects.create(user=form_user, total_area=total_area, number_of_levels=number_of_levels,
                                    buildingType=Building_and_Condition_Types.get_building_type(int(buildingType)), 
                                    condition=Building_and_Condition_Types.get_condition_type(int(condition)),
                                    ceilings=ceilings, parking=parking, firealarm=firealarm, security=security, video_surveillance=video_surveillance, 
                                    alarm_system=alarm_system, optics=optics, predicted_price=prediction)

            return render(request, "main/index.html", {"form": prediction_form, "prediction": prediction, "krysha": property_on_krysha_with_similar_price, "toShow": toShow})
    else:
        prediction_form = PredictionForm()

    return render(request, "main/index.html", {"form": prediction_form})


# HISTORY PAGE
def history(request):

    if request.user.is_anonymous:
        return render(request, "main/history.html")
    else:    
        history_notes = History.objects.filter(user=request.user)
        return render(request, "main/history.html", {"history": history_notes})
    

# ANALYTICS PAGE
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):


    number_of_history_notes = History.objects.all().count()

    number_of_history_notes_anonymous = list(History.objects.values_list('user',  flat=True))
    number_of_history_notes_anonymous = Counter(number_of_history_notes_anonymous)[None]

    number_of_history_notes_registered = number_of_history_notes - number_of_history_notes_anonymous

    buildingType_column = list(History.objects.values_list('buildingType',  flat=True))
    condition_column = list(History.objects.values_list('condition',  flat=True))
    total_area_column = list(History.objects.values_list('total_area',  flat=True))
    predicted_price_column = list(History.objects.values_list('predicted_price',  flat=True))

    average_kzt_per_meter = int(sum(predicted_price_column) / sum(total_area_column))

    building_types_data = [list(Counter(buildingType_column).keys()), list(Counter(buildingType_column).values())]
    condition_types_data = [list(Counter(condition_column).keys()), list(Counter(condition_column).values())]


    context = {
        "building_types_keys": building_types_data[0],
        "building_types_values": building_types_data[1],

        "condition_types_keys": condition_types_data[0],
        "condition_types_values": condition_types_data[1],

        "number_of_history_notes": number_of_history_notes,
        "number_of_history_notes_anonymous": number_of_history_notes_anonymous,
        "number_of_history_notes_registered": number_of_history_notes_registered,

        "average_kzt_per_meter": average_kzt_per_meter,


    }
    return render(request, "main/analytics.html", context=context)
    

# REGISTRAION
def signup(request):

    if request.method == "POST":
        registration_form = RegistrationForm(request.POST)  

        if registration_form.is_valid():

            username = registration_form.cleaned_data['username']
            fname = registration_form.cleaned_data['fname']
            lname = registration_form.cleaned_data['lname']
            email = registration_form.cleaned_data['email']
            pass1 = registration_form.cleaned_data['pass1']
            pass2 = registration_form.cleaned_data['pass2']

            if User.objects.filter(username=username):
                messages.error(request, "Username already exists!")
                return redirect("signup")

            if User.objects.filter(email=email):
                messages.error(request, "Email already exists!")
                return redirect("signup")

            if pass1 != pass2:
                messages.error(request, "Passwords did not match!")
                return redirect("signup")
            
            if not username.isalnum():
                messages.error(request, "Username must be Alpha-Numeric!")
                return redirect("signup")
            
            if len(pass1) < 6:
                messages.error(request, "Password must be longer than 6 values!")
                return redirect("signup")
        
            new_user = User.objects.create_user(username, email, pass1)
            new_user.first_name = fname
            new_user.last_name = lname
            new_user.save()
            
            return redirect('signin')

    else:
        registration_form = RegistrationForm()  
    return render(request, "main/signup.html", {"form": registration_form})


# LOGIN
def signin(request):

    if request.method == "POST":
        login_form = LoginForm(request.POST)   
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)                
                return redirect('index')
            else:
                messages = "Wrong login or password"
                return redirect('signin')

    else:
        login_form = LoginForm()

    return render(request, "main/signin.html", {"form": login_form})


# SIGN OUT
def signout(request):
    logout(request)
    return redirect('index')