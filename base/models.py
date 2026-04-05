from django.db import models
from django.contrib.auth.models import User

class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=15)
    aadhaar_no = models.CharField(max_length=20)
    address = models.TextField()
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=5, choices=[
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ])
    weight = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    hospital_id = models.CharField(max_length=50)
    icu_availability = models.BooleanField(default=False)
    mobile_van_availability = models.BooleanField(default=False)
    hospital_contact_no = models.CharField(max_length=15)
    hospital_email_id = models.EmailField()

    def __str__(self):
        return self.hospital_name

class DonationRequest(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending', choices=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ])
    donation_status = models.CharField(max_length=20, default='Pending', choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ])
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    request_date = models.DateTimeField(auto_now_add=True)
    slot_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Request by {self.donor.name} - {self.status}"

class HospitalBloodRequest(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5)
    is_emergency = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.hospital.hospital_name} - {self.blood_group} (Emergency: {self.is_emergency})"

class OrganDonor(models.Model):
    donor = models.OneToOneField(Donor, on_delete=models.CASCADE)
    donate_heart = models.BooleanField(default=False)
    donate_kidneys = models.BooleanField(default=False)
    donate_liver = models.BooleanField(default=False)
    donate_eyes = models.BooleanField(default=False)
    donate_lungs = models.BooleanField(default=False)
    donate_pancreas = models.BooleanField(default=False)
    pledge_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Organ Pledge: {self.donor.name}"

class Achievement(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='achievements/')
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.location}"

class GalleryImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image by {self.user.username}"
