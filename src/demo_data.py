import pandas as pd
import random

def generate_demo_data(num_samples=100, output_file="data/demo_phishing_emails.csv"):
    """
    Generate demo phishing and non-phishing email data for quick testing.
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

    data = []

    for _ in range(num_samples // 2):
        # Phishing email
        template = random.choice(phishing_templates)
        link = random.choice(fake_links)
        email = template.format(link=link)
        data.append({"text": email, "label": 1})

        # Non-phishing email
        template = random.choice(non_phishing_templates)
        data.append({"text": template, "label": 0})

    # Shuffle the data
    random.shuffle(data)

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Demo data generated and saved to {output_file}")
    print(f"Generated {len(df)} samples: {len(df[df['label']==1])} phishing, {len(df[df['label']==0])} non-phishing")

if __name__ == "__main__":
    generate_demo_data()
