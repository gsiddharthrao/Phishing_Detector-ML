import pandas as pd
import random

def generate_demo_data(num_samples=100, output_file="data/demo_phishing_emails.csv"):
    """
    Generate demo phishing and non-phishing email data for quick testing, including headers.
    """
    phishing_templates = [
        "Urgent: Your account has been compromised. Click here to reset your password: {link}",
        "Congratulations! You've won a prize. Claim it now: {link}",
        "Security Alert: Unusual activity detected. Verify your account: {link}",
        "Your package is delayed. Update shipping info: {link}",
        "Bank Alert: Suspicious transaction. Confirm details: {link}",
        "Important: Update your payment information: {link}",
        "You've been selected for a special offer. Act now: {link}",
        "Password reset required. Click the link: {link}",
        "Your subscription is expiring. Renew now: {link}",
        "Verify your email address: {link}"
    ]

    non_phishing_templates = [
        "Meeting reminder: Team standup at 10 AM tomorrow.",
        "Invoice attached for services rendered last month.",
        "Thank you for your recent purchase. Your order has shipped.",
        "Weekly newsletter: Latest updates from our department.",
        "Project update: The deadline has been extended to next Friday.",
        "Vacation request approved. Enjoy your time off!",
        "System maintenance scheduled for this weekend.",
        "New employee onboarding session next Tuesday.",
        "Quarterly report attached for your review.",
        "Happy birthday! Hope you have a great day."
    ]

    fake_links = [
        "http://secure-bank-login.com",
        "http://account-verify.net",
        "http://prize-claim.org",
        "http://password-reset.info",
        "http://shipping-update.biz"
    ]

    phishing_senders = [
        "support@bank-alert.com",
        "security@account-verify.net",
        "admin@password-reset.info",
        "alert@secure-login.org",
        "noreply@prize-claim.biz"
    ]

    non_phishing_senders = [
        "hr@company.com",
        "team@project.org",
        "billing@services.net",
        "newsletter@updates.com",
        "admin@internal.biz"
    ]

    data = []

    for _ in range(num_samples // 2):
        # Phishing email with headers
        template = random.choice(phishing_templates)
        link = random.choice(fake_links)
        sender = random.choice(phishing_senders)
        subject = random.choice(["Security Alert", "Account Verification Required", "Urgent Action Needed", "Password Reset", "Suspicious Activity"])
        to = "user@example.com"
        date = "Mon, 13 Sep 2025 09:33:00 -0700"
        headers = f"From: {sender}\nTo: {to}\nSubject: {subject}\nDate: {date}\n\n"
        body = template.format(link=link)
        full_email = headers + body
        data.append({"text": full_email, "label": 1})

        # Non-phishing email with headers
        template = random.choice(non_phishing_templates)
        sender = random.choice(non_phishing_senders)
        subject = random.choice(["Meeting Reminder", "Invoice", "Update", "Report", "Birthday"])
        to = "user@example.com"
        date = "Mon, 13 Sep 2025 09:33:00 -0700"
        headers = f"From: {sender}\nTo: {to}\nSubject: {subject}\nDate: {date}\n\n"
        body = template
        full_email = headers + body
        data.append({"text": full_email, "label": 0})

    # Shuffle the data
    random.shuffle(data)

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Demo data generated and saved to {output_file}")
    print(f"Generated {len(df)} samples: {len(df[df['label']==1])} phishing, {len(df[df['label']==0])} non-phishing")

if __name__ == "__main__":
    generate_demo_data()
