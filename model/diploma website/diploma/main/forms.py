from django import forms


class PredictionForm(forms.Form):

    total_area = forms.FloatField(label="Square")
    number_of_levels = forms.IntegerField(label="Number of Levels")
    
    buildingType = forms.ChoiceField(label="Building Type", choices=[
        (0, 'other'), (1, 'brick'), (2, 'wooden'), (3, 'panel'), (4, 'monolithic')
    ])
    # 0 - иное
    # 1 - кирпичное
    # 2 - деревянное
    # 3 - панельное
    # 4 - монолитное

    condition = forms.ChoiceField(label="Condition", choices=[
        (0, 'not completed'), (1, 'open plan'), (2, 'average'), (3, 'rough finish'), (4, 'good'), (5, 'needs renovation')
    ])
    # 0 - не достроено
    # 1 - свободная планировка
    # 2 - среднее
    # 3 - черновая отделка
    # 4 - хорошее
    # 5 - требует ремонта
    
    ceilings = forms.FloatField(label="Ceilings")
    parking = forms.BooleanField(label="Parking",  required=False)
    firealarm = forms.BooleanField(label="Firealarm", required=False)
    security = forms.BooleanField(label="Security",  required=False)
    video_surveillance = forms.BooleanField(label="Video Surveillance",  required=False)
    alarm_system = forms.BooleanField(label="Alarm System",  required=False)
    optics = forms.BooleanField(label="Optics", required=False)


class RegistrationForm(forms.Form):
    username = forms.CharField(label="Create username")
    fname = forms.CharField(label="Your Firstname")
    lname = forms.CharField(label="Your Lastname")
    email = forms.CharField(label="Your Email")
    pass1 = forms.CharField(label="Create a Password")
    pass2 = forms.CharField(label="Confirm Your Password")


class LoginForm(forms.Form):
    username = forms.CharField(label="Enter your username")
    password = forms.CharField(label="Enter your Password")
                    