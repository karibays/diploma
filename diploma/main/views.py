from django.shortcuts import render, redirect
# import tensorflow as tf
import numpy as np
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import PredictionForm, RegistrationForm, LoginForm
from .models import History
from sklearn.preprocessing import StandardScaler

Scaler = StandardScaler()

def index(request):

    if request.method == "POST":
        prediction_form = PredictionForm(request.POST)
        toShow = False
    
        if prediction_form.is_valid():
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
            print(total_area, number_of_levels, buildingType, condition, ceilings, parking, firealarm, security, video_surveillance, alarm_system, optics)
            prediction = predict(total_area, number_of_levels, buildingType, condition, ceilings, parking, firealarm, security, video_surveillance, alarm_system, optics)
            toShow = True

            property_on_krysha_with_similar_price = f"https://krisha.kz/prodazha/pomeshhenija/?das[price][from]={int(prediction * 0.95)}&das[price][to]={int(prediction * 1.05)}"

            form_user = None
            if not request.user.is_anonymous:
                form_user = User.objects.get(username=request.user)

            History.objects.create(user=form_user, total_area=total_area, number_of_levels=number_of_levels, buildingType=buildingType, condition=condition, 
                        ceilings=ceilings, parking=parking, firealarm=firealarm, security=security, video_surveillance=video_surveillance, 
                        alarm_system=alarm_system, optics=optics, predicted_price=prediction)

            return render(request, "main/index.html", {"form": prediction_form, "prediction": prediction, "krysha": property_on_krysha_with_similar_price, "toShow": toShow})
    else:
        prediction_form = PredictionForm()

    return render(request, "main/index.html", {"form": prediction_form})


def predict(total_area, number_of_levels, buildingType, condition, ceilings, parking, firealarm, security, video_surveillance, alarm_system, optics):

    # model = tf.keras.models.load_model(r'C:\Users\karib\Desktop\diploma\models\model_v2')

    parking = int(parking == True)
    firealarm = int(firealarm == True)
    security = int(security == True)
    video_surveillance = int(video_surveillance == True)
    alarm_system = int(alarm_system == True)
    optics = int(optics == True)

    data_to_predict = np.array([total_area, number_of_levels, buildingType, condition, ceilings, parking, firealarm, security, video_surveillance, alarm_system, optics]).astype(float)


    # data = scale_data(data_to_predict)
    # data = np.expand_dims(data, 0)

    # prediction = model.predict(data)[0][0]
    # prediction = tf.math.exp(prediction).numpy()
    # prediction = prediction - prediction % 10000
    return sum(data_to_predict)


def scale_data(data):
    means = np.array([6.68714563e+02, 2.00598526e+00, 9.23103213e-01, 2.42481203e+00,
    3.46777119e+00, 6.44907724e-01, 3.63636364e-01, 2.50512645e-01,
    4.13192071e-01, 4.03964457e-01, 8.20232399e-02])

    vars = np.array([2.67955554e+05, 7.00102538e-01, 1.58499597e+00, 4.78296604e+00,
    4.97651762e-01, 2.29001752e-01, 2.31404959e-01, 1.87756060e-01,
    2.43147910e-01, 2.40777174e-01, 7.52954280e-02])
    
    return (data - means) / (vars ** 0.5)


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
        
            new_user = User.objects.create_user(username, email, pass1)
            new_user.first_name = fname
            new_user.last_name = lname
            new_user.save()
            messages.success(request, "Your account has been successfully created")
            
            return redirect('signin')

    else:
        registration_form = RegistrationForm()  
    
    return render(request, "main/signup.html", {"form": registration_form})


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
                messages.error(request, "Wrong login or password")
                return redirect('signin')

    else:
        login_form = LoginForm()

    return render(request, "main/signin.html", {"form": login_form})


def signout(request):
    logout(request)
    return redirect('index')


def history(request):

    if request.user.is_anonymous:
        return render(request, "main/history.html")
    else:    
        history_notes = History.objects.filter(user=request.user)
        return render(request, "main/history.html", {"history": history_notes})