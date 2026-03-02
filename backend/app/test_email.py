from email_service import send_alert_confirmation

send_alert_confirmation(
    to_email="professor_email@gmail.com",  # ← put real email here
    product_name="Python Crash Course",
    target_price=300,
    current_price=3533,
    best_platform="Amazon",
    best_url="https://www.amazon.in"
)