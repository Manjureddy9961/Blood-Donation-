import requests
import threading

def _send_emergency_sms(msg):
    target_number = "+917382783093"
    print(f"\n[EMERGENCY NOTIFICATION TRIGGERED]")
    print(f"To: {target_number}")
    print(f"Message: {msg}\n")
    try:
        # Textbelt allows 1 free SMS per day per IP address using the 'textbelt' key
        resp = requests.post('https://textbelt.com/text', {
            'phone': target_number,
            'message': msg,
            'key': 'textbelt',
        })
        print(f"Textbelt SMS Status: {resp.json()}")
    except Exception as e:
        print(f"Failed to send SMS via Textbelt: {e}")

def send_emergency_notification(hospital_name, blood_group):
    """
    Sends an SMS asynchronously using Textbelt API for emergency requests.
    """
    message_body = f"URGENT: {hospital_name} needs {blood_group} blood immediately! Please check dashboard."
    t = threading.Thread(target=_send_emergency_sms, args=(message_body,))
    t.start()
