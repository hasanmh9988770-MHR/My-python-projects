import os
import smtplib
import secrets
import string
import time
from email.message import EmailMessage
from dotenv import load_dotenv  # Loads variables from your .env file

# 1. Initialize environment variables
load_dotenv()

# 2. Configuration Constants
OTP_LENGTH = 6
OTP_EXPIRY_SECONDS = 120  # 2 minutes
MAX_ATTEMPTS = 3


def generate_otp(length=OTP_LENGTH):
    """Generates a cryptographically secure random OTP."""
    return ''.join(secrets.choice(string.digits) for _ in range(length))


def send_email_otp(receiver_email, otp):
    """Fetches credentials from .env and sends the email."""
    sender_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASS")

    if not sender_email or not app_password:
        raise ValueError("❌ Error: EMAIL_USER or EMAIL_PASS not found in your .env file.")

    msg = EmailMessage()
    msg["Subject"] = "Your Secure Verification Code"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(f"""
Your OTP is: {otp}

This code will expire in 2 minutes.
Do not share this code with anyone for security reasons.
""")

    # Using Port 587 with STARTTLS for Gmail compatibility
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)


def verify_otp(real_otp, created_time):
    """Handles the user input and expiry logic."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        user_input = input(f"\nEnter OTP (Attempt {attempt}/{MAX_ATTEMPTS}): ").strip()

        # Immediate Expiry Check
        elapsed_time = time.time() - created_time
        if elapsed_time > OTP_EXPIRY_SECONDS:
            print(f"❌ OTP expired {int(elapsed_time - OTP_EXPIRY_SECONDS)} seconds ago. Please restart.")
            return False

        if user_input == real_otp:
            print("✅ Verified successfully! Access granted.")
            return True
        else:
            if attempt < MAX_ATTEMPTS:
                print(f"❌ Incorrect OTP. You have {MAX_ATTEMPTS - attempt} attempts left.")

    print("\n🚫 Too many failed attempts. Session locked.")
    return False


def main():
    print("--- Secure OTP System ---")
    receiver_email = input("Enter your email address: ").strip()

    otp = generate_otp()
    created_time = time.time()

    try:
        print("📩 Sending email... please wait.")
        send_email_otp(receiver_email, otp)
        print(f"✅ OTP sent to {receiver_email}!")

        verify_otp(otp, created_time)

    except Exception as e:
        print(f"⚠️ System Error: {e}")


if __name__ == "__main__":
    main()

## to run this in terminal: python "My Projects/OTP verification.py"
## create a .env files and input: EMAIL_USER=your@gmail.com
# EMAIL_PASS=your16characterapppass
## python 3.9 ## check git staus (.env file will never show) and git check-ignore -v .env [for safe coding]