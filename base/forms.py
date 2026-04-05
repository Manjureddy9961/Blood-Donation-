from django import forms
from .models import Donor, Hospital, DonationRequest, OrganDonor, GalleryImage
from django.contrib.auth.models import User

class DonorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = Donor
        fields = ['mobile_no', 'aadhaar_no', 'address', 'date_of_birth', 'blood_group', 'weight']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        donor = super().save(commit=False)
        donor.user = user
        donor.name = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
        if commit:
            donor.save()
        return donor

class HospitalRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    class Meta:
        model = Hospital
        fields = ['hospital_name', 'location', 'hospital_id', 'icu_availability', 'mobile_van_availability', 'hospital_contact_no']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        hospital = super().save(commit=False)
        hospital.user = user
        hospital.hospital_email_id = self.cleaned_data['email'] 
        if commit:
            hospital.save()
        return hospital

class OrganDonationForm(forms.ModelForm):
    class Meta:
        model = OrganDonor
        fields = ['donate_heart', 'donate_kidneys', 'donate_liver', 'donate_eyes', 'donate_lungs', 'donate_pancreas']
        widgets = {
            'donate_heart': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'donate_kidneys': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'donate_liver': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'donate_eyes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'donate_lungs': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'donate_pancreas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', 'caption']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Invalid unsupported format")
        return image
