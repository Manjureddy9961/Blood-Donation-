from django.contrib import admin
from django.shortcuts import render
from .models import Donor, Hospital, DonationRequest, OrganDonor, Achievement, GalleryImage

@admin.action(description='Print Selected Donors')
def print_donor_data(modeladmin, request, queryset):
    headers = ['Name', 'Mobile', 'Blood Group', 'Address']
    data = []
    for obj in queryset:
        data.append([obj.name, obj.mobile_no, obj.blood_group, obj.address])
    
    return render(request, 'admin/print_view.html', {
        'title': 'Donor List',
        'headers': headers,
        'data': data
    })

@admin.action(description='Print Selected Requests')
def print_donation_requests(modeladmin, request, queryset):
    headers = ['Donor', 'Hospital', 'Status', 'Request Date']
    data = []
    for obj in queryset:
        hospital_name = obj.hospital.hospital_name if obj.hospital else '-'
        data.append([obj.donor.name, hospital_name, obj.status, obj.request_date.strftime('%Y-%m-%d')])
    
    return render(request, 'admin/print_view.html', {
        'title': 'Donation Requests',
        'headers': headers,
        'data': data
    })

class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_no', 'blood_group', 'user')
    search_fields = ('name', 'mobile_no')
    actions = [print_donor_data]

class HospitalAdmin(admin.ModelAdmin):
    list_display = ('hospital_name', 'location', 'hospital_contact_no', 'icu_availability')
    search_fields = ('hospital_name', 'location')

from django.utils.html import format_html
from django.urls import reverse

class DonationRequestAdmin(admin.ModelAdmin):
    list_display = ('donor', 'hospital', 'status', 'request_date', 'completion_action')
    list_filter = ('status', 'donation_status', 'request_date')
    actions = [print_donation_requests]
    
    def completion_action(self, obj):
        if obj.donation_status == 'Pending':
            url = reverse('admin_mark_donation_completed', args=[obj.id])
            return format_html(
                '<a class="button" href="{}" style="background-color: #28a745; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px;">Mark as Completed Donation</a>',
                url
            )
        elif obj.donation_status == 'Completed' and obj.qr_code:
            return format_html(
                '<div style="text-align: center;">'
                '<img src="{}" width="60" height="60" style="display: block; margin: 0 auto; margin-bottom: 5px;" />'
                '<a href="{}" download class="button" style="background-color: #007bff; color: white; padding: 3px 8px; text-decoration: none; border-radius: 3px; font-size: 12px;">Download QR</a>'
                '</div>',
                obj.qr_code.url,
                obj.qr_code.url
            )
        return obj.donation_status
        
    completion_action.short_description = 'Donation Status / Actions'

admin.site.register(Donor, DonorAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(DonationRequest, DonationRequestAdmin)
admin.site.register(OrganDonor)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date_posted')
    search_fields = ('title', 'location')
    list_filter = ('location', 'date_posted')

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'uploaded_at')
    search_fields = ('user__username', 'caption')
