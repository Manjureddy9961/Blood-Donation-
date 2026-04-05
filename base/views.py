from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import DonorRegistrationForm, HospitalRegistrationForm, OrganDonationForm, GalleryImageForm
from .models import Donor, Hospital, DonationRequest, OrganDonor, Achievement, GalleryImage
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register_donor(request):
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            donor = form.save()
            login(request, donor.user)
            return redirect('donor_dashboard')
    else:
        form = DonorRegistrationForm()
    return render(request, 'auth/register_donor.html', {'form': form})

def register_hospital(request):
    if request.method == 'POST':
        form = HospitalRegistrationForm(request.POST)
        if form.is_valid():
            hospital = form.save()
            login(request, hospital.user)
            return redirect('hospital_dashboard')
    else:
        form = HospitalRegistrationForm()
    return render(request, 'auth/register_hospital.html', {'form': form})

from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful')
            if hasattr(user, 'donor'):
                return redirect('donor_dashboard')
            elif hasattr(user, 'hospital'):
                return redirect('hospital_dashboard')
            elif user.is_superuser:
                 return redirect('/admin/')
            else:
                return redirect('index') # Fallback
        else:
            # Check for missing fields
            if not request.POST.get('username') or not request.POST.get('password'):
                 messages.error(request, 'Missing the credentials')
            else:
                 messages.error(request, 'Invalid credentials')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def donor_dashboard(request):
    if not hasattr(request.user, 'donor'):
        return redirect('index')
    
    donor = request.user.donor
    
    # Organ Donation Logic
    try:
        organ_donor = donor.organdonor
    except OrganDonor.DoesNotExist:
        organ_donor = None

    if request.method == 'POST':
        if 'book_slot' in request.POST:
             slot_date = request.POST.get('slot_date')
             DonationRequest.objects.create(donor=donor, slot_date=slot_date, status='Pending')
             return redirect('donor_dashboard')
        elif 'pledge_organs' in request.POST:
            if organ_donor:
                organ_form = OrganDonationForm(request.POST, instance=organ_donor)
            else:
                organ_form = OrganDonationForm(request.POST)
                
            if organ_form.is_valid():
                organ_pledge = organ_form.save(commit=False)
                organ_pledge.donor = donor
                organ_pledge.save()
                return redirect('donor_dashboard')
        elif 'upload_image' in request.POST:
            form = GalleryImageForm(request.POST, request.FILES)
            if form.is_valid():
                img = form.save(commit=False)
                img.user = request.user
                img.save()
                return redirect('donor_dashboard')

    if organ_donor:
        organ_form = OrganDonationForm(instance=organ_donor)
    else:
        organ_form = OrganDonationForm()

    history = DonationRequest.objects.filter(donor=donor)
    
    return render(request, 'dashboard/donor.html', {
        'donor': donor, 
        'history': history,
        'organ_form': organ_form,
        'organ_donor': organ_donor,
        'gallery_images': GalleryImage.objects.filter(user=request.user),
        'image_form': GalleryImageForm()
    })

@login_required
def hospital_dashboard(request):
    if not hasattr(request.user, 'hospital'):
        return redirect('index')
    
    hospital = request.user.hospital
    
    if request.method == 'POST':
        if 'upload_image' in request.POST:
            form = GalleryImageForm(request.POST, request.FILES)
            if form.is_valid():
                img = form.save(commit=False)
                img.user = request.user
                img.save()
                return redirect('hospital_dashboard')
        elif 'raise_request' in request.POST:
            blood_group = request.POST.get('blood_group')
            is_emergency = request.POST.get('is_emergency') == 'on'
            from .models import HospitalBloodRequest
            HospitalBloodRequest.objects.create(
                hospital=hospital, 
                blood_group=blood_group, 
                is_emergency=is_emergency
            )
            if is_emergency:
                from .notifications import send_emergency_notification
                send_emergency_notification(hospital.hospital_name, blood_group)
            return redirect('hospital_dashboard')

    # Pending blood requests
    requests = DonationRequest.objects.filter(status='Pending')
    
    # Organ Stats
    organ_stats = {
        'Hearts': OrganDonor.objects.filter(donate_heart=True).count(),
        'Kidneys': OrganDonor.objects.filter(donate_kidneys=True).count(),
        'Livers': OrganDonor.objects.filter(donate_liver=True).count(),
        'Eyes': OrganDonor.objects.filter(donate_eyes=True).count(),
        'Lungs': OrganDonor.objects.filter(donate_lungs=True).count(),
        'Pancreases': OrganDonor.objects.filter(donate_pancreas=True).count(),
    }
    
    from .models import HospitalBloodRequest
    active_hospital_requests = HospitalBloodRequest.objects.filter(hospital=hospital).order_by('-created_at')
    
    return render(request, 'dashboard/hospital.html', {
        'hospital': hospital, 
        'requests': requests,
        'organ_stats': organ_stats,
        'active_hospital_requests': active_hospital_requests,
        'gallery_images': GalleryImage.objects.filter(user=request.user),
        'image_form': GalleryImageForm()
    })

@login_required
def update_request_status(request, request_id, status):
    if not hasattr(request.user, 'hospital'):
        # Only hospitals (or admin) can approve
        return redirect('index')
        
    donation_request = DonationRequest.objects.get(id=request_id)
    donation_request.status = status
    donation_request.hospital = request.user.hospital # Assign to this hospital
    donation_request.save()
    
    # Blockchain Integration
    if status == 'Accepted':
        try:
            from .blockchain_utils import log_donation_to_blockchain
            log_donation_to_blockchain(
                donor_id=str(donation_request.donor.id),
                blood_group=donation_request.donor.blood_group,
                donation_date=str(donation_request.request_date.date()),
                hospital_name=donation_request.hospital.hospital_name,
                verification_status='Verified & Accepted'
            )
        except Exception as e:
            print(f"Blockchain logging failed: {e}")
            
    return redirect('hospital_dashboard')

def achievements_view(request):
    achievements = Achievement.objects.all().order_by('-date_posted')
    return render(request, 'base/achievements.html', {'achievements': achievements})

@login_required
def delete_image(request, image_id):
    image = GalleryImage.objects.get(id=image_id)
    if image.user == request.user:
        image.delete()
    
    if hasattr(request.user, 'donor'):
        return redirect('donor_dashboard')
    elif hasattr(request.user, 'hospital'):
         return redirect('hospital_dashboard')
    return redirect('index')

from django.http import JsonResponse

@login_required
def recommend_donors_view(request):
    if not hasattr(request.user, 'hospital'):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    blood_group = request.GET.get('blood_group')
    location = request.GET.get('location')
    
    if not blood_group or not location:
        return JsonResponse({'error': 'Missing blood_group or location'}, status=400)
        
    try:
        from .ml_model import recommend_top_donors
        recommendations = recommend_top_donors(blood_group=blood_group, location=location)
        return JsonResponse({'recommendations': recommendations})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.urls import reverse
from django.shortcuts import get_object_or_404

@login_required
def mark_donation_completed(request, request_id):
    if not request.user.is_superuser:
        return redirect('index')
    
    donation_request = get_object_or_404(DonationRequest, id=request_id)
    
    if donation_request.donation_status == 'Pending':
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        verify_url = request.build_absolute_uri(reverse('verify_qr', args=[donation_request.id]))
        qr.add_data(verify_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        file_name = f'qr_donation_{donation_request.id}.png'
        
        donation_request.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)
        donation_request.donation_status = 'Completed'
        donation_request.save()
        messages.success(request, f'Donation marked as completed for {donation_request.donor.name}. QR code generated.')
        
    return redirect('admin:base_donationrequest_changelist')

def verify_qr(request, request_id):
    donation = get_object_or_404(DonationRequest, id=request_id)
    return render(request, 'base/verify_qr.html', {'donation': donation})
