import random

class PhishingScenario:
    def __init__(self, id, type, sender, subject, body, correct_action, difficulty, indicators, feedback, tip, xp, category):
        self.id = id
        self.type = type
        self.sender = sender
        self.subject = subject
        self.body = body
        self.correct_action = correct_action
        self.difficulty = difficulty
        self.indicators = indicators
        self.feedback = feedback
        self.tip = tip
        self.xp = xp
        self.category = category

SIMULATION_SCENARIOS = [
    # --- EASY SCENARIOS (Obvious) ---
    {
        "id": 1,
        "type": "phishing",
        "sender": "HR Dept <hr-update@workday-portal-secure.net>",
        "subject": "URGENT: Salary Review",
        "body": "<p>Click here to view your salary increase: <a href='#' class='fake-link' data-url='http://workday-portal-secure.net/login'>View Now</a></p>",
        "correct_action": "report",
        "difficulty": "Easy",
        "indicators": ["Suspicious Domain", "Urgency"],
        "feedback": "<strong>Phishing!</strong> 'workday-portal-secure.net' is fake.",
        "tip": "Always check the domain name.",
        "xp": 50,
        "category": "Urgency"
    },
    {
        "id": 2,
        "type": "phishing",
        "sender": "Winner <lottery@free-money.com>",
        "subject": "You won the lottery!",
        "body": "<p>Claim your $1,000,000 prize now! <a href='#' class='fake-link' data-url='http://claim-prize.com'>Claim Here</a></p>",
        "correct_action": "report",
        "difficulty": "Easy",
        "indicators": ["Too good to be true", "Generic greeting"],
        "feedback": "<strong>Phishing!</strong> You didn't enter a lottery. If it's too good to be true, it is.",
        "tip": "Lottery scams are common. Never click.",
        "xp": 50,
        "category": "Greed"
    },
    {
        "id": 3,
        "type": "phishing",
        "sender": "CEO <ceo@gmail.com>",
        "subject": "Wire Transfer Needed",
        "body": "<p>I need you to wire $50k immediately for a secret project. Don't tell anyone.</p>",
        "correct_action": "report",
        "difficulty": "Easy",
        "indicators": ["Personal Email (Gmail)", "Financial Request"],
        "feedback": "<strong>Phishing!</strong> CEOs don't use personal Gmail for wire transfers.",
        "tip": "Verify unusual financial requests offline.",
        "xp": 50,
        "category": "CEO Fraud"
    },
    {
        "id": 4,
        "type": "safe",
        "sender": "IT Support <support@deepshield.com>",
        "subject": "Server Maintenance Notice",
        "body": "<p>Just a heads up, servers will be down this Saturday at 2 AM.</p>",
        "correct_action": "archive",
        "difficulty": "Easy",
        "indicators": ["Internal Sender", "Informational Only"],
        "feedback": "<strong>Safe.</strong> Standard internal info.",
        "tip": "Informational emails with no links are usually safe.",
        "xp": 30,
        "category": "Internal"
    },
    {
        "id": 5,
        "type": "phishing",
        "sender": "Netflix <support@netflix-verify-payment.com>",
        "subject": "Payment Failed",
        "body": "<p>Your subscription is suspended. <a href='#' class='fake-link' data-url='http://netflix-verify.com'>Update Payment</a></p>",
        "correct_action": "report",
        "difficulty": "Easy",
        "indicators": ["Spoofed Domain", "Threat of suspension"],
        "feedback": "<strong>Phishing!</strong> Netflix uses netflix.com, not 'netflix-verify-payment.com'.",
        "tip": "Check the URL before solving 'payment issues'.",
        "xp": 50,
        "category": "Impersonation"
    },
    {
        "id": 11, "type": "phishing", "sender": "Amazon <orders@amazon-shipping-update.com>", "subject": "Order #555 Delayed", "body": "<p>Your order is held. <a href='#' class='fake-link' data-url='http://amazon-shipping-update.com'>Resolve</a></p>", "correct_action": "report", "difficulty": "Easy", "indicators": ["Fake Domain"], "feedback": "Fake Amazon domain.", "tip": "Check orders in the Amazon app, not via email links.", "xp": 50, "category": "Impersonation"
    },
    {
        "id": 12, "type": "safe", "sender": "HR <hr@deepshield.com>", "subject": "Holiday Calendar", "body": "<p>Attached is the 2026 holiday calendar.</p>", "correct_action": "archive", "difficulty": "Easy", "indicators": ["Internal", "Expected content"], "feedback": "Safe internal email.", "tip": "Internal docs are fine if from trusted sources.", "xp": 30, "category": "Internal"
    },
    {
        "id": 13, "type": "phishing", "sender": "Admin <admin@company-portal.info>", "subject": "Reset Password", "body": "<p>Expires in 24h. <a href='#' class='fake-link' data-url='http://bit.ly/reset'>Reset</a></p>", "correct_action": "report", "difficulty": "Easy", "indicators": [".info domain", "Bit.ly link"], "feedback": "Admin portal won't use .info or bit.ly.", "tip": "Hover over short links (bit.ly) to be careful.", "xp": 50, "category": "Credentials"
    },
    {
        "id": 14, "type": "phishing", "sender": "IRS <tax@irs-gov.org>", "subject": "Tax Refund Pending", "body": "<p>Claim your refund. <a href='#' class='fake-link' data-url='http://irs-gov.org'>Claim</a></p>", "correct_action": "report", "difficulty": "Easy", "indicators": [".org domain (IRS is .gov)"], "feedback": "IRS is .gov, not .org.", "tip": "Government agencies use .gov.", "xp": 50, "category": "Gov Spoof"
    },
    {
        "id": 15, "type": "safe", "sender": "Google Calendar <calendar-notification@google.com>", "subject": "Meeting Reminder", "body": "<p>Team Sync at 10 AM.</p>", "correct_action": "archive", "difficulty": "Easy", "indicators": ["Legit Google sender"], "feedback": "Standard calendar reminder.", "tip": "Auto-generated reminders are common.", "xp": 30, "category": "Productivity"
    },

    # --- MEDIUM SCENARIOS (Tricky) ---
    {
        "id": 21,
        "type": "phishing",
        "sender": "Microsoft 365 <security@microsoft-auth-center.com>",
        "subject": "Unusual Sign-in: Russia",
        "body": "<p>Login detected from Moscow. <button class='btn btn-primary fake-btn' data-url='http://microsoft-auth-center.com/reset'>Secure Account</button></p>",
        "correct_action": "report",
        "difficulty": "Medium",
        "indicators": ["Spoofed Domain", "Geo-fear"],
        "feedback": "Real Microsoft alerts link to microsoft.com.",
        "tip": "Don't panic at 'Hacker' alerts.",
        "xp": 75,
        "category": "Spoofing"
    },
    {
        "id": 22,
        "type": "phishing",
        "sender": "CEO <ceo-private@gmail.com>",
        "subject": "Quick Favor (Gift Cards)",
        "body": "<p>In a meeting. Need 5x $100 Apple cards for client. Reimburse later.</p>",
        "correct_action": "report",
        "difficulty": "Medium",
        "indicators": ["Gmail sender", "Gift Card request"],
        "feedback": "Classic CEO Fraud.",
        "tip": "Gift cards = Scam. Always.",
        "xp": 75,
        "category": "CEO Fraud"
    },
    {
        "id": 23,
        "type": "safe",
        "sender": "LinkedIn <messages-noreply@linkedin.com>",
        "subject": "New Job Alerts",
        "body": "<p>30 jobs match your profile. <a href='#' class='fake-link' data-url='https://www.linkedin.com/jobs'>View</a></p>",
        "correct_action": "archive",
        "difficulty": "Medium",
        "indicators": ["Legit Domain", "Legit Link"],
        "feedback": "Real LinkedIn email.",
        "tip": "Check the URL path.",
        "xp": 50,
        "category": "Social"
    },
    {
        "id": 24,
        "type": "phishing",
        "sender": "Dropbox <share@dropbox.net>",
        "subject": "File Shared: Financials.xlsx",
        "body": "<p>Click to download. <a href='#' class='fake-link' data-url='http://dropbox-secure-share.com/login'>Download</a></p>",
        "correct_action": "report",
        "difficulty": "Medium",
        "indicators": ["dropbox.net (should be .com)", "Mismatched Link"],
        "feedback": "Dropbox is dropbox.com. Watch the extension.",
        "tip": "File shares are common vectors for malware.",
        "xp": 75,
        "category": "File Sharing"
    },
    {
        "id": 25,
        "type": "phishing",
        "sender": "IT Helpdesk <support@deepshieId.com>",
        "subject": "Password Expiry",
        "body": "<p>Reset now. <a href='#' class='fake-link' data-url='http://sso-portal.com'>Reset</a></p>",
        "correct_action": "report",
        "difficulty": "Medium",
        "indicators": ["Typosquatting (Capital I instead of l)", "Generic Link"],
        "feedback": "Look closely: deepshieId (Capital i) vs deepshield (lowercase L).",
        "tip": "Typosquatting relies on visual tricks.",
        "xp": 75,
        "category": "Typosquatting"
    },
    {
        "id": 26, "type": "safe", "sender": "Slack <notification@slack.com>", "subject": "New message from Team", "body": "<p>You have a new message.</p>", "correct_action": "archive", "difficulty": "Medium", "indicators": ["Real Sender"], "feedback": "Legit Slack notification.", "tip": "Verify notification settings if unsure.", "xp": 50, "category": "Productivity"
    },
    {
        "id": 27, "type": "phishing", "sender": "Zoom <meetings@zoom-video-conferencing.com>", "subject": "Missed Meeting", "body": "<p>View recording: <a href='#' class='fake-link' data-url='http://zoom-download.com/malware.exe'>Recording.mp4</a></p>", "correct_action": "report", "difficulty": "Medium", "indicators": ["Fake Zoom domain", "Download link"], "feedback": "Zoom uses zoom.us.", "tip": "Meetings don't send .exe files.", "xp": 75, "category": "Malware"
    },
    {
        "id": 28, "type": "phishing", "sender": "Apple <support@apple-id-recovery.net>", "subject": "Account Locked", "body": "<p>Unlock now. <a href='#' class='fake-link' data-url='http://apple-id-recovery.net'>Unlock</a></p>", "correct_action": "report", "difficulty": "Medium", "indicators": ["Fake Domain"], "feedback": "Apple uses apple.com.", "tip": "Account lockouts? Go to the site directly.", "xp": 75, "category": "Impersonation"
    },
    {
        "id": 29, "type": "safe", "sender": "GitHub <noreply@github.com>", "subject": "[Repo] Pull Request Merged", "body": "<p>PR #42 merged.</p>", "correct_action": "archive", "difficulty": "Medium", "indicators": ["Real Domain"], "feedback": "Safe GitHub notification.", "tip": "Dev tools are often spoofed, but this one is real.", "xp": 50, "category": "Dev"
    },
    {
        "id": 30, "type": "phishing", "sender": "PayPal <service@paypal-billing-issue.com>", "subject": "Unauthorized Transaction", "body": "<p>Dispute charge of $500. <a href='#' class='fake-link' data-url='http://paypal-support.com'>Dispute</a></p>", "correct_action": "report", "difficulty": "Medium", "indicators": ["Fake Domain"], "feedback": "PayPal uses paypal.com.", "tip": "Billing issues are high-stress traps.", "xp": 75, "category": "Finance"
    },

    # --- HARD SCENARIOS (Subtle) ---
    {
        "id": 31,
        "type": "phishing",
        "sender": "DocuSign <dse@docusign.net.Docs.com>",
        "subject": "Please Sign: NDA",
        "body": "<p>Review document. <a href='#' class='fake-link' data-url='http://bit.ly/3x89s1'>Review</a></p>",
        "correct_action": "report",
        "difficulty": "Hard",
        "indicators": ["Subdomain Spoofing (Ends in Docs.com)", "Bit.ly link"],
        "feedback": "Subdomain spoofing: 'docusign.net.Docs.com' is actually 'Docs.com'.",
        "tip": "Read URLs fro Right-to-Left.",
        "xp": 100,
        "category": "Spoofing"
    },
    {
        "id": 32,
        "type": "phishing",
        "sender": "IT <admin@deepshield.com.mail-server-update.net>",
        "subject": "Policy Update",
        "body": "<p>Read new policy.</p>",
        "correct_action": "report",
        "difficulty": "Hard",
        "indicators": ["Long Subdomain"],
        "feedback": "Ends in .net, not .com.",
        "tip": "The last part of the domain is the real one.",
        "xp": 100,
        "category": "Spoofing"
    },
    {
        "id": 33,
        "type": "safe",
        "sender": "Amazon.com <shipment-tracking@amazon.com>",
        "subject": "Your Order Shipped",
        "body": "<p>Track here. <a href='#' class='fake-link' data-url='https://www.amazon.com/gp/css/shiptrack'>Track</a></p>",
        "correct_action": "archive",
        "difficulty": "Hard",
        "indicators": ["Real Domain", "Real Link"],
        "feedback": "Actually safe. Amazon emails look cluttered but check headers.",
        "tip": "Not every Amazon email is fake. Check the SSL cert/URL.",
        "xp": 100,
        "category": "Impersonation"
    },
    {
        "id": 34,
        "type": "phishing",
        "sender": "Colleague <bob.smith@deepshield-lab.com>",
        "subject": "Project files",
        "body": "<p>Hey, checking out this new tool. <a href='#' class='fake-link' data-url='http://deepshield-lab.com/install'>Install</a></p>",
        "correct_action": "report",
        "difficulty": "Hard",
        "indicators": ["Simulated Internal Domain 'deepshield-lab.com'", "Shadow IT"],
        "feedback": "Domain 'deepshield-lab.com' is not 'deepshield.com'.",
        "tip": "Lookalike domains are dangerous.",
        "xp": 100,
        "category": "Typosquatting"
    },
    {
        "id": 35,
        "type": "phishing",
        "sender": "Vendor <billing@vendor-portal.com>",
        "subject": "Invoice 9921",
        "body": "<p>Attached. <a href='#' class='fake-link' data-url='http://onedrive-live.com/download'>Invoice.pdf.exe</a></p>",
        "correct_action": "report",
        "difficulty": "Hard",
        "indicators": ["Double extension .pdf.exe", "Fake One Drive"],
        "feedback": "File is .exe, not .pdf.",
        "tip": "Always check file extensions.",
        "xp": 100,
        "category": "Malware"
    },
    {
        "id": 36, "type": "safe", "sender": "DeepShield Admin <admin@deepshield.com>", "subject": "Q3 Report", "body": "<p>Here is the report.</p>", "correct_action": "archive", "difficulty": "Hard", "indicators": ["Internal"], "feedback": "Safe internal.", "tip": "Trust but verify.", "xp": 50, "category": "Internal"
    },
    {
        "id": 37, "type": "phishing", "sender": "Support <support@micros0ft.com>", "subject": "Ticket Closed", "body": "<p>Reopen?</p>", "correct_action": "report", "difficulty": "Hard", "indicators": ["Zero instead of O"], "feedback": "micros0ft.com (Zero).", "tip": "Homograph attacks replace letters with lookalikes.", "xp": 100, "category": "Typosquatting"
    },
    {
        "id": 38, "type": "phishing", "sender": "Internal <hr@deepshieId.com>", "subject": "Bonus", "body": "<p>Claim.</p>", "correct_action": "report", "difficulty": "Hard", "indicators": ["Capital I for l"], "feedback": "Typosquatting.", "tip": "Watch for I vs l.", "xp": 100, "category": "Typosquatting"
    },
    {
        "id": 39, "type": "safe", "sender": "Stripe <notifications@stripe.com>", "subject": "Payment Received", "body": "<p>$50.00 received.</p>", "correct_action": "archive", "difficulty": "Hard", "indicators": ["Real Stripe"], "feedback": "Safe.", "tip": "Transactional emails are often real.", "xp": 50, "category": "Finance"
    },
    {
        "id": 40, "type": "phishing", "sender": "Legal <legal@law-firm-secure.com>", "subject": "Lawsuit", "body": "<p>Urgent. <a href='#' class='fake-link' data-url='http://law-firm-secure.com/case'>View Case</a></p>",
        "correct_action": "report",
        "difficulty": "Hard",
        "indicators": ["Urgency", "Generic Legal Threat"],
        "feedback": "Legal threats via email are usually scams to prompt rash action.",
        "tip": "Call your legal team first.",
        "xp": 100,
        "category": "Legal"
    }
]

def get_random_scenarios(count=5, difficulty=None):
    """Returns a random list of scenarios, optionally filtered by difficulty."""
    pool = SIMULATION_SCENARIOS
    if difficulty:
        pool = [s for s in SIMULATION_SCENARIOS if s['difficulty'].lower() == difficulty.lower()]
        
        # Fallback if request count > available exact matches
        # Fill with other scenarios but try to prioritize similar difficulty? 
        # For now, just duplicate or fill with randoms if needed, but uniqueness is better.
        
        if len(pool) < count:
            remaining = [s for s in SIMULATION_SCENARIOS if s not in pool]
            needed = count - len(pool)
            if remaining:
                pool.extend(random.sample(remaining, min(needed, len(remaining))))
            
    # Sample without replacement if possible
    return random.sample(pool, min(count, len(pool)))
