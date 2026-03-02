import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ✅ Put your Gmail credentials here
SENDER_EMAIL = "p68223595@gmail.com"
SENDER_PASSWORD = "glio ahal lepr ubxy"  # App password (spaces OK)


def send_alert_confirmation(
    to_email: str,
    product_name: str,
    target_price: float,
    current_price: float,
    best_platform: str,
    best_url: str
):
    """Send a beautiful HTML confirmation email when alert is set"""

    subject = f"✅ Price Alert Set — {product_name} | PriceSenseAI"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8"/>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
    <body style="margin:0;padding:0;background:#F0F8FF;font-family:'Courier New',monospace;">

      <!-- Header -->
      <div style="background:linear-gradient(135deg,#87CEEB,#4BA3CC);padding:40px 20px;text-align:center;">
        <div style="font-size:60px;margin-bottom:10px;">👻</div>
        <h1 style="color:white;margin:0;font-size:28px;letter-spacing:4px;">PRICESENSEAI</h1>
        <p style="color:rgba(255,255,255,0.85);margin:6px 0 0;font-size:12px;letter-spacing:2px;">
          SMART BOOK PRICE COMPARISON
        </p>
      </div>

      <!-- Body -->
      <div style="max-width:560px;margin:0 auto;padding:30px 20px;">

        <!-- Success card -->
        <div style="background:white;border:2px solid #87CEEB;border-radius:16px;padding:30px;margin-bottom:20px;box-shadow:0 4px 20px rgba(135,206,235,0.2);">
          <div style="font-size:40px;text-align:center;margin-bottom:15px;">🔔</div>
          <h2 style="text-align:center;color:#1a3a4a;font-size:18px;letter-spacing:3px;margin:0 0 8px;">
            ALERT SUCCESSFULLY SET!
          </h2>
          <p style="text-align:center;color:#6699bb;font-size:13px;margin:0;">
            We'll notify you the moment the price drops!
          </p>
        </div>

        <!-- Book details -->
        <div style="background:white;border:2px solid #B8DFF0;border-radius:16px;padding:25px;margin-bottom:20px;">
          <div style="font-size:11px;letter-spacing:3px;color:#4BA3CC;margin-bottom:12px;">📚 BOOK DETAILS</div>

          <div style="margin-bottom:15px;">
            <div style="font-size:11px;color:#6699bb;letter-spacing:2px;margin-bottom:4px;">BOOK NAME</div>
            <div style="font-size:16px;color:#1a3a4a;font-weight:bold;">{product_name}</div>
          </div>

          <div style="display:flex;gap:20px;flex-wrap:wrap;">
            <div style="flex:1;min-width:140px;">
              <div style="font-size:11px;color:#6699bb;letter-spacing:2px;margin-bottom:4px;">CURRENT BEST PRICE</div>
              <div style="font-size:22px;color:#2980b9;font-weight:bold;">₹{int(current_price):,}</div>
              <div style="font-size:11px;color:#6699bb;">ON {best_platform.upper()}</div>
            </div>
            <div style="flex:1;min-width:140px;">
              <div style="font-size:11px;color:#6699bb;letter-spacing:2px;margin-bottom:4px;">YOUR TARGET PRICE</div>
              <div style="font-size:22px;color:#27ae60;font-weight:bold;">₹{int(target_price):,}</div>
              <div style="font-size:11px;color:#27ae60;">YOU'LL SAVE ₹{int(current_price - target_price):,}</div>
            </div>
          </div>
        </div>

        <!-- CTA Button -->
        <div style="text-align:center;margin-bottom:20px;">
          <a href="{best_url}"
             style="display:inline-block;background:#4BA3CC;color:white;text-decoration:none;
                    padding:14px 32px;border-radius:999px;font-size:13px;letter-spacing:3px;">
            VIEW CURRENT DEAL →
          </a>
        </div>

        <!-- Info box -->
        <div style="background:#EEF8FD;border:1px solid #B8DFF0;border-radius:12px;padding:18px;margin-bottom:20px;">
          <div style="font-size:11px;letter-spacing:2px;color:#4BA3CC;margin-bottom:8px;">ℹ️ WHAT HAPPENS NEXT?</div>
          <ul style="margin:0;padding-left:18px;color:#2d6080;font-size:13px;line-height:2;">
            <li>Our system checks prices every few hours</li>
            <li>When price drops below ₹{int(target_price):,}, you get an email</li>
            <li>You can then grab the deal before it expires!</li>
          </ul>
        </div>

      </div>

      <!-- Footer -->
      <div style="text-align:center;padding:20px;color:#6699bb;font-size:11px;letter-spacing:2px;">
        <div style="margin-bottom:6px;">PRICESENSEAI · MIET INSTITUTE OF ENGINEERING & TECHNOLOGY</div>
        <div>Tamanna Sharma · Bhumika Shan · Manya Khajuria · Anirudh Singh</div>
        <div style="margin-top:8px;color:#B8DFF0;">2025–26</div>
      </div>

    </body>
    </html>
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"PriceSenseAI 👻 <{SENDER_EMAIL}>"
        msg["To"] = to_email

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD.replace(" ", ""))
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

        print(f"✅ Email sent to {to_email}")
        return True

    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False