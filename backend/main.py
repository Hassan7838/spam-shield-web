from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, User, Email
from pydantic import BaseModel
import hashlib
from datetime import datetime
from model import predict_spam
from fastapi.responses import RedirectResponse, HTMLResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class CheckSpam(BaseModel):
    email_text: str

class SendEmail(BaseModel):
    user_id: int
    recipient: str
    subject: str
    body: str

base_url = os.getenv(
            "BASE_URL",
            "https://tenley-pyroligneous-nonascertainably.ngrok-free.dev"
        )

# controllers

@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed = hashlib.sha256(user.password.encode()).hexdigest()
    db_user = User(username=user.username, email=user.email, password_hash=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created"}


@app.post("/login")
def login(user: Login, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or db_user.password_hash != hashlib.sha256(user.password.encode()).hexdigest():
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"user_id": db_user.id}


@app.post("/check-spam")
def check_spam(data: CheckSpam):
    is_spam = predict_spam(data.email_text)
    return {"is_spam": bool(is_spam)}


@app.post("/send-email")
def send_email(data: SendEmail, db: Session = Depends(get_db)):
    print(f"\n{'='*60}")
    print(f"New email request from user {data.user_id}")
    print(f"   To: {data.recipient}")
    print(f"   Subject: {data.subject}")
    spam = predict_spam(data.body)
    try:
        # Save email first
        db_email = Email(
            user_id=data.user_id,
            recipient=data.recipient,
            subject=data.subject,
            body=data.body,
            is_spam = int(spam),
            sent_at=datetime.now()
        )
        db.add(db_email)
        db.commit()
        db.refresh(db_email)

        print(f"Email saved to DB with ID: {db_email.id}")

        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        sender_email = os.getenv("SENDER_EMAIL", "devhassan7838@gmail.com")
        sender_password = os.getenv("SENDER_PASSWORD", "fmdh oyki jalv pgfv")
        

        # Create email
        msg = MIMEMultipart("alternative")
        msg["Subject"] = data.subject
        msg["From"] = sender_email
        msg["To"] = data.recipient

        view_button = f"""
        <a href="{base_url}/view/{db_email.id}"
           style="
             display:inline-block;
             padding:12px 20px;
             background:#2563eb;
             color:white;
             text-decoration:none;
             border-radius:6px;
             font-weight:bold;">
           View Message
        </a>
        """

        html_body = f"""
        <p>You have received a secure message.</p>
        {view_button}
        """

        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, data.recipient, msg.as_string())

        print(f"Email sent successfully")
        print(f"{'='*60}\n")

        return {"message": "Email sent and saved", "email_id": db_email.id}

    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return {"message": "Email saved (SMTP failed)", "email_id": db_email.id}


@app.get("/emails")
def get_emails(user_id: int = None, db: Session = Depends(get_db)):
    if not user_id or user_id <= 0:
        return []

    emails = db.query(Email).filter(Email.user_id == user_id).all()
    return [
        {
            "id": e.id,
            "recipient": e.recipient,
            "subject": e.subject,
            "sent_at": str(e.sent_at),
            "opened_at": str(e.opened_at) if e.opened_at else None
        }
        for e in emails
    ]


#  BUTTON-BASED TRACKING
@app.get("/view/{email_id}")
def view_email(email_id: int, db: Session = Depends(get_db)):
    email = db.query(Email).filter(Email.id == email_id).first()

    if email and not email.opened_at:
        email.opened_at = datetime.now()
        email.status = "OPENED"

        
    email.click_count += 1
    db.commit()
    return RedirectResponse(url=f"{base_url}/content/{email_id}")


@app.get("/content/{email_id}", response_class=HTMLResponse)
def show_email_content(email_id: int, db: Session = Depends(get_db)):
    email = db.query(Email).filter(Email.id == email_id).first()

    if not email:
        return "<h3>Email not found</h3>"

    # views

    return f"""
    <html>
      <body style="font-family: Arial; padding: 30px;">
        <h2>Subject : {email.subject}</h2><br><br>
        <p>Message : {email.body}</p>
      </body>
    </html>
    """
