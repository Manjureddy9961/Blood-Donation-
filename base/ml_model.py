import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder
from datetime import date
from django.utils import timezone
from .models import Donor, DonationRequest

def get_donor_data():
    """
    Fetches donor data from the database and prepares it for the ML model.
    """
    donors = Donor.objects.all()
    data = []
    
    for donor in donors:
        # Calculate last donation days ago
        last_donation = DonationRequest.objects.filter(
            donor=donor, 
            status='Accepted'
        ).order_by('-request_date').first()
        
        if last_donation:
            days_since = (timezone.now().date() - last_donation.request_date.date()).days
        else:
            # If never donated, give a high number so they are prioritized 
            # (they are available to donate)
            days_since = 9999
            
        data.append({
            'donor_id': donor.id,
            'name': donor.name,
            'blood_group': donor.blood_group,
            'location': donor.address,  # Assuming address represents location here
            'days_since_last_donation': days_since
        })
        
    return pd.DataFrame(data)

def recommend_top_donors(blood_group, location, preferred_days_since=90, top_n=5):
    """
    Uses KNN to recommend the top matching donors based on:
    - Exact Blood Group match (filtered first, or highly weighted)
    - Location similarity (encoded)
    - Days since last donation (longer is better, or at least > 90)
    """
    df = get_donor_data()
    
    if df.empty:
        return []
        
    # We heavily penalize basic mismatch in blood group by filtering first
    # because blood group must match (or be compatible, but for simplicity we use exact match)
    df_filtered = df[df['blood_group'] == blood_group].copy()
    
    if df_filtered.empty:
        return []
        
    # Encode Location
    # In a real app we'd use Geocoding. Here we use LabelEncoder for simplicity
    le_loc = LabelEncoder()
    # Fit on all locations to ensure the input location can be transformed
    le_loc.fit(df['location'].tolist() + [location])
    
    df_filtered['loc_encoded'] = le_loc.transform(df_filtered['location'])
    input_loc_encoded = le_loc.transform([location])[0]
    
    # We will use NearestNeighbors based on [loc_encoded, days_since_last_donation_normalized]
    # For days_since_last_donation, we want larger numbers to be "closer" to preferred_days_since if we invert it, 
    # but simple KNN looks for exact distance.
    # To make longer days_since better, we can set our 'ideal' input to a very high number (e.g., 9999).
    
    features = df_filtered[['loc_encoded', 'days_since_last_donation']]
    
    # Input vector
    input_vector = [[input_loc_encoded, 9999]]
    
    # Model
    knn = NearestNeighbors(n_neighbors=min(top_n, len(df_filtered)), metric='euclidean')
    knn.fit(features)
    
    distances, indices = knn.kneighbors(input_vector)
    
    recommended_donors = []
    for idx in indices[0]:
        donor_info = df_filtered.iloc[idx]
        recommended_donors.append({
            'id': donor_info['donor_id'],
            'name': donor_info['name'],
            'blood_group': donor_info['blood_group'],
            'location': donor_info['location'],
            'days_since_last_donation': donor_info['days_since_last_donation'],
        })
        
    return recommended_donors
