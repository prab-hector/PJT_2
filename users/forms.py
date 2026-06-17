from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator 
from storage.models import Teammates

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True) 
    
    phone_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(r'^\d+$', message="Phone number must contain only numbers."),
            MinLengthValidator(10, message="Phone number must be exactly 10 digits long."), 
            MaxLengthValidator(10, message="Phone number must be exactly 10 digits long.") 
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Enter 10-digit number'})
    )
    about = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4, 
            'placeholder': 'Tell us something about your profile...',
            'class': 'form-control' # Bootstrap styling
        }),
        label="About Paragraph"
    )
    branch = forms.CharField(required=True, max_length=30)
    year = forms.CharField(required=False, max_length=30)
    division = forms.CharField(required=True, max_length=20)
    domain = forms.CharField(required=True, max_length=30)
    rfid_num = forms.CharField(required=True,max_length=8)
    current_project = forms.CharField(required=False, max_length=30)

    class Meta:
        model = User
        fields = ['username', 'email'] 

        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            
            from storage.models import Teammates
            Teammates.objects.create(
                author=user,
                name=user.username,
                branch=self.cleaned_data.get('branch'),
                division=self.cleaned_data.get('division'),
                current_project=self.cleaned_data.get('current_project'),
                domain=self.cleaned_data.get('domain'),
                year=self.cleaned_data.get('year'),
                about=self.cleaned_data.get('about'),
                rfid_num = self.cleaned_data.get('rfid_num'),
                phone_number=self.cleaned_data.get('phone_number')
            )
        return user
    

class ProfileUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email']

class StorageUpdateForm(forms.ModelForm):
    
    division = forms.CharField(required=True)
    domain = forms.CharField(required=True)
    branch = forms.CharField(required=True)
    phone_number = forms.CharField(
        required=True,
        validators=[
            RegexValidator(r'^\d+$', message="Phone number must contain only numbers."),
            MinLengthValidator(10, message="Phone number must be exactly 10 digits long."), 
            MaxLengthValidator(10, message="Phone number must be exactly 10 digits long.") 
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Enter 10-digit number'})
    )
    year = forms.CharField(required=False, max_length=30)
    current_project = forms.CharField(required=False, max_length=30)
    rfid_num =forms.CharField(required=True,max_length=8)

    about = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4, 
            'placeholder': 'Tell us something about your profile...',
            'class': 'form-control' # Bootstrap styling
        }),
        label="About Paragraph"
    )
    class Meta:
        model = Teammates
        # This list ensures ONLY these 5 fields are rendered and processed
        fields = ['email', 'division', 'domain', 'branch','rfid_num','phone_number','year','current_project']

