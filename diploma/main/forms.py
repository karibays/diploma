from django import forms


class PredictionForm(forms.Form):

    total_area = forms.FloatField(label="Square")
    number_of_levels = forms.IntegerField(label="Number of Levels")
    
    buildingType = forms.ChoiceField(label="Building Type", choices=[
        (0, 'other'), (1, 'brick'), (2, 'wooden'), (3, 'panel'), (4, 'monolithic')
    ])

    condition = forms.ChoiceField(label="Condition", choices=[
        (0, 'not completed'), (1, 'open plan'), (2, 'average'), (3, 'rough finish'), (4, 'good'), (5, 'needs renovation')
    ])
    
    ceilings = forms.FloatField(label="Ceilings")
    parking = forms.BooleanField(label="Parking",  required=False)
    firealarm = forms.BooleanField(label="Firealarm", required=False)
    security = forms.BooleanField(label="Security",  required=False)
    video_surveillance = forms.BooleanField(label="Video Surveillance",  required=False)
    alarm_system = forms.BooleanField(label="Alarm System",  required=False)
    optics = forms.BooleanField(label="Optics", required=False)


class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'input-text with-border', 'placeholder': 'Create username'}))

    fname = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'input-text with-border', 'placeholder': 'Your Firstname'}))

    lname = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'input-text with-border', 'placeholder': 'Your Lastname'}))

    email = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'input-text with-border', 'placeholder': 'Your Email'}))
    
    pass1 = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'input-text with-border', 'placeholder': 'Create a Password'}))

    pass2 = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'input-text with-border', 'placeholder': 'Confirm Your Password'}))


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'input-text with-border', 'placeholder': 'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'input-text with-border', 'placeholder': 'Enter your password'}))
                    