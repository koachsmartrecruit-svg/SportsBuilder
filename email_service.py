"""
Email Service for SportsBuilder
Handles transactional emails using SendGrid
"""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
import os

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
FROM_EMAIL = os.environ.get('FROM_EMAIL', 'noreply@sportsbuilder.com')
FROM_NAME = os.environ.get('FROM_NAME', 'SportsBuilder')
SITE_URL = os.environ.get('SITE_URL', 'https://www.sportsbuilder.com')

def send_email(to_email, subject, html_content, text_content=None):
    """
    Send email using SendGrid
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML email body
        text_content: Plain text email body (optional)
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not SENDGRID_API_KEY:
        print("⚠️ SendGrid API key not configured. Email not sent.")
        return False
    
    try:
        message = Mail(
            from_email=Email(FROM_EMAIL, FROM_NAME),
            to_emails=To(to_email),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        
        if text_content:
            message.add_content(Content("text/plain", text_content))
        
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        
        print(f"✅ Email sent to {to_email}: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


def send_welcome_email(user_email, user_name=None):
    """
    Send welcome email to new users
    
    Args:
        user_email: User's email address
        user_name: User's name (optional)
    
    Returns:
        bool: True if sent successfully
    """
    name = user_name or user_email.split('@')[0]
    
    subject = f"Welcome to SportsBuilder, {name}! 🎉"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #e63946, #1d3557); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; }}
            .button {{ display: inline-block; background: #e63946; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to SportsBuilder! 🏆</h1>
            </div>
            <div class="content">
                <h2>Hi {name},</h2>
                <p>Thanks for joining SportsBuilder! We're excited to help you create amazing sports websites.</p>
                
                <h3>What's Next?</h3>
                <ul>
                    <li>Choose from 4 professional templates</li>
                    <li>Customize colors, fonts, and content</li>
                    <li>Upload your logo and images</li>
                    <li>Publish your site instantly</li>
                </ul>
                
                <a href="{SITE_URL}/dashboard" class="button">Go to Dashboard →</a>
                
                <p>Need help? Check out our <a href="{SITE_URL}/docs">documentation</a> or reply to this email.</p>
                
                <p>Happy building!<br>The SportsBuilder Team</p>
            </div>
            <div class="footer">
                <p>© 2026 SportsBuilder. All rights reserved.</p>
                <p>You received this email because you signed up for SportsBuilder.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Welcome to SportsBuilder, {name}!
    
    Thanks for joining SportsBuilder! We're excited to help you create amazing sports websites.
    
    What's Next?
    - Choose from 4 professional templates
    - Customize colors, fonts, and content
    - Upload your logo and images
    - Publish your site instantly
    
    Go to Dashboard: {SITE_URL}/dashboard
    
    Need help? Check out our documentation or reply to this email.
    
    Happy building!
    The SportsBuilder Team
    """
    
    return send_email(user_email, subject, html_content, text_content)


def send_site_published_email(user_email, site_name, site_url):
    """
    Send notification when a site is published
    
    Args:
        user_email: User's email address
        site_name: Name of the published site
        site_url: Public URL of the site
    
    Returns:
        bool: True if sent successfully
    """
    subject = f"🎉 Your site '{site_name}' is now live!"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; }}
            .button {{ display: inline-block; background: #10b981; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .url-box {{ background: white; padding: 15px; border-left: 4px solid #10b981; margin: 20px 0; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Your Site is Live!</h1>
            </div>
            <div class="content">
                <h2>Congratulations!</h2>
                <p>Your site <strong>{site_name}</strong> has been published and is now live on the internet!</p>
                
                <div class="url-box">
                    <strong>Your Site URL:</strong><br>
                    <a href="{site_url}">{site_url}</a>
                </div>
                
                <a href="{site_url}" class="button">View Your Site →</a>
                
                <h3>Share Your Site:</h3>
                <ul>
                    <li>Share the link on social media</li>
                    <li>Add it to your email signature</li>
                    <li>Include it in your marketing materials</li>
                </ul>
                
                <p>Want to make changes? You can edit your site anytime from your <a href="{SITE_URL}/dashboard">dashboard</a>.</p>
                
                <p>Best regards,<br>The SportsBuilder Team</p>
            </div>
            <div class="footer">
                <p>© 2026 SportsBuilder. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Congratulations! Your Site is Live!
    
    Your site '{site_name}' has been published and is now live on the internet!
    
    Your Site URL: {site_url}
    
    Share Your Site:
    - Share the link on social media
    - Add it to your email signature
    - Include it in your marketing materials
    
    Want to make changes? You can edit your site anytime from your dashboard: {SITE_URL}/dashboard
    
    Best regards,
    The SportsBuilder Team
    """
    
    return send_email(user_email, subject, html_content, text_content)


def send_password_reset_email(user_email, reset_token):
    """
    Send password reset email
    
    Args:
        user_email: User's email address
        reset_token: Password reset token
    
    Returns:
        bool: True if sent successfully
    """
    reset_url = f"{SITE_URL}/reset-password?token={reset_token}"
    
    subject = "Reset Your SportsBuilder Password"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #1d3557; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; }}
            .button {{ display: inline-block; background: #e63946; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔒 Password Reset Request</h1>
            </div>
            <div class="content">
                <h2>Reset Your Password</h2>
                <p>We received a request to reset your SportsBuilder password.</p>
                
                <p>Click the button below to reset your password:</p>
                
                <a href="{reset_url}" class="button">Reset Password →</a>
                
                <div class="warning">
                    <strong>⚠️ Important:</strong>
                    <ul>
                        <li>This link expires in 1 hour</li>
                        <li>If you didn't request this, please ignore this email</li>
                        <li>Your password won't change until you create a new one</li>
                    </ul>
                </div>
                
                <p>If the button doesn't work, copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #666;">{reset_url}</p>
                
                <p>Need help? Reply to this email or contact our support team.</p>
                
                <p>Best regards,<br>The SportsBuilder Team</p>
            </div>
            <div class="footer">
                <p>© 2026 SportsBuilder. All rights reserved.</p>
                <p>If you didn't request a password reset, please ignore this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Reset Your SportsBuilder Password
    
    We received a request to reset your SportsBuilder password.
    
    Click this link to reset your password:
    {reset_url}
    
    Important:
    - This link expires in 1 hour
    - If you didn't request this, please ignore this email
    - Your password won't change until you create a new one
    
    Need help? Reply to this email or contact our support team.
    
    Best regards,
    The SportsBuilder Team
    """
    
    return send_email(user_email, subject, html_content, text_content)


def send_contact_form_notification(admin_email, sender_name, sender_email, message):
    """
    Send notification when someone submits a contact form
    
    Args:
        admin_email: Admin email to receive notification
        sender_name: Name of person who submitted form
        sender_email: Email of person who submitted form
        message: Message content
    
    Returns:
        bool: True if sent successfully
    """
    subject = f"New Contact Form Submission from {sender_name}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #1d3557; color: white; padding: 20px; }}
            .content {{ background: #f8f9fa; padding: 30px; }}
            .info-box {{ background: white; padding: 15px; border-left: 4px solid #2563eb; margin: 20px 0; }}
            .message-box {{ background: white; padding: 20px; border: 1px solid #ddd; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>📧 New Contact Form Submission</h2>
            </div>
            <div class="content">
                <div class="info-box">
                    <strong>From:</strong> {sender_name}<br>
                    <strong>Email:</strong> <a href="mailto:{sender_email}">{sender_email}</a>
                </div>
                
                <div class="message-box">
                    <strong>Message:</strong><br><br>
                    {message}
                </div>
                
                <p><a href="mailto:{sender_email}">Reply to {sender_name} →</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(admin_email, subject, html_content)


# Test function
if __name__ == "__main__":
    print("🧪 Testing Email Service")
    print(f"SendGrid API Key: {'✅ Configured' if SENDGRID_API_KEY else '❌ Not configured'}")
    print(f"From Email: {FROM_EMAIL}")
    print(f"Site URL: {SITE_URL}")
    
    # Uncomment to test sending an email
    # send_welcome_email("test@example.com", "Test User")
