import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def create_and_send_reservation(**kwargs):
    # Create the reservation dictionary
    reservation_request = {
        f'reservation_request_{datetime.datetime.now()}': kwargs
    }

    # Set up the SMTP server
    s = smtplib.SMTP(host='your_host', port='your_port')
    s.starttls()
    s.login('your_email', 'your_password')

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = 'your_email'
    msg['To'] = 'recipient_email'
    msg['Subject'] = 'Reservation Request'
    msg.attach(MIMEText(str(reservation_request)))

    # Send the email
    s.send_message(msg)
    s.quit()

    return reservation_request

'''
{
  "name": "create_and_send_reservation",
  "description": "Create a reservation request and send it via email",
  "parameters": {
    "type": "object",
    "properties": {
      "full_name_and_birthdate": {
        "type": "string",
        "description": "Full name(s) and birthdate(s)"
      },
      "number_of_travelers": {
        "type": "integer",
        "description": "Number of people traveling"
      },
      "preferred_room_type": {
        "type": "string",
        "description": "Preferred room type (single, double, triple, etc.)"
      },
      "transport_and_special_requests": {
        "type": "string",
        "description": "Transportation and special requests (e.g., special meal requests or facilities for the disabled)"
      },
      "contact_information": {
        "type": "string",
        "description": "Your contact information (email and phone number)"
      },
      "preferred_tour_name": {
        "type": "string",
        "description": "Preferred tour name"
      }
    },
    "required": [
      "full_name_and_birthdate",
      "contact_information",
      "preferred_tour_name"
    ]
  }
}'''