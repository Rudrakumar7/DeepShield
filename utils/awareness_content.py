# awareness_content.py

AWARENESS_TOPICS = [
    {
        'id': 'phishing',
        'title': 'Phishing Attacks',
        'icon': '🎣',
        'difficulty': 'Beginner',
        'read_time': '5 min',
        'tags': ['Email', 'Scams', 'Social Engineering'],
        'overview': 'Phishing is a deceptive attempt to steal sensitive information like passwords or credit card numbers by masquerading as a trustworthy entity.',
        'why_matters': '90% of all data breaches start with a phishing email. Falling for one can compromise your entire organization.',
        'examples': [
            'Email claiming your account is locked and asking you to click a link.',
            'SMS (Smishing) claiming you have a package delivery issue.',
            'CEO Fraud: Email pretending to be your boss asking for urgent wire transfer.'
        ],
        'prevention': [
            'Verify the sender\'s email address carefully.',
            'Hover over links to see the actual URL before clicking.',
            'Enable Multi-Factor Authentication (MFA).',
            'Never share sensitive info via email.'
        ],
        'quiz': [
            {
                'question': 'What is the most common indicator of a phishing email?',
                'options': ['It comes from a known contact', 'It creates a false sense of urgency', 'It has a blue background'],
                'answer': 1
            },
            {
                'question': 'What should you do if you receive a suspicious email?',
                'options': ['Reply and ask if it is real', 'Click the link to check', 'Report it to IT and delete it'],
                'answer': 2
            }
        ]
    },
    {
        'id': 'passwords',
        'title': 'Password Security',
        'icon': '🔑',
        'difficulty': 'Beginner',
        'read_time': '4 min',
        'tags': ['Authentication', 'Basics'],
        'overview': 'Weak or reused passwords are the easiest way for hackers to breach your accounts.',
        'why_matters': 'Credential stuffing attacks use leaked passwords from one site to unlock accounts on others.',
        'examples': [
            'Using "password123" or "admin".',
            'Using the same password for banking and social media.',
            'Writing passwords on sticky notes.'
        ],
        'prevention': [
            'Use a Password Manager.',
            'Create passwords with 12+ characters, mixed case, numbers, and symbols.',
            'Use unique passwords for every account.',
            'Enable 2FA wherever possible.'
        ],
        'quiz': [
            {
                'question': 'Which password is strongest?',
                'options': ['P@ssword1', 'Correct-Horse-Battery-Staple-88', 'admin123'],
                'answer': 1
            },
            {
                'question': 'Why is 2FA important?',
                'options': ['It makes logging in faster', 'It adds a second layer of defense even if your password is stolen', 'It prevents you from forgetting your password'],
                'answer': 1
            }
        ]
    },
    {
        'id': 'deepfakes',
        'title': 'Deepfakes & AI',
        'icon': '🎭',
        'difficulty': 'Intermediate',
        'read_time': '6 min',
        'tags': ['AI', 'Fraud', 'Biometrics'],
        'overview': 'AI-generated synthetic media (audio/video) used to impersonate people.',
        'why_matters': 'Deepfakes are now used in "CEO Fraud" calls and to bypass biometric verification.',
        'examples': [
            'A video call where a "coworker" asks for money but looks slightly off.',
            'Audio clips of family members claiming to be in trouble (virtual kidnapping scams).'
        ],
        'prevention': [
            'Check for unnatural blinking or lip-sync issues.',
            'Listen for robotic or monotonous audio.',
            'Verify suspicious requests through a second channel (call them back).'
        ],
        'quiz': [
            {
                'question': 'How can you spot a deepfake video?',
                'options': ['The video quality is always poor', 'Unnatural blinking or lighting inconsistencies', 'It is always in black and white'],
                'answer': 1
            }
        ]
    },
    {
        'id': 'social_engineering',
        'title': 'Social Engineering',
        'icon': '🗣️',
        'difficulty': 'Intermediate',
        'read_time': '7 min',
        'tags': ['Psychology', 'Scams'],
        'overview': 'Manipulating people into performing actions or divulging confidential information.',
        'why_matters': 'Humans are often the weakest link in security, stronger than any firewall.',
        'examples': [
            'Tailgating: Following someone into a secure building.',
            'Pretexting: Calling IT support pretending to be an employee who lost their password.',
            'Baiting: Leaving an infected USB drive in a parking lot.'
        ],
        'prevention': [
            'Be skeptical of urgent requests (e.g., "Act Now!").',
            'Verify the identity of unknown individuals.',
            'Follow verify-then-trust procedures.'
        ],
         'quiz': [
            {
                'question': 'What is "Tailgating"?',
                'options': ['Driving too close to a car', 'Following an authorized person into a secure area', 'Emailing a CEO'],
                'answer': 1
            }
        ]
    },
    {
        'id': 'malware',
        'title': 'Malware & Ransomware',
        'icon': '🦠',
        'difficulty': 'Advanced',
        'read_time': '8 min',
        'tags': ['Viruses', 'Ransomware', 'Technical'],
        'overview': 'Malicious software designed to harm, exploit, or hold your data hostage.',
        'why_matters': 'Ransomware can lock you out of your own files and demand payment, often causing permanent data loss.',
        'examples': [
            'WannaCry: Infected 200k+ computers worldwide.',
            'Trojan: Software that looks legit but contains malware.',
            'Spyware: Silent software that tracks your keystrokes.'
        ],
        'prevention': [
            'Keep OS and software updated (patching).',
            'Use reputable antivirus software.',
            'Backup data regularly (3-2-1 rule).',
            'Avoid downloading files from untrusted sources.'
        ],
        'quiz': [
            {
                'question': 'What is Ransomware?',
                'options': ['Free software', 'Malware that encrypts files and demands payment', 'A type of firewall'],
                'answer': 1
            }
        ]
    },
     {
        'id': 'wifi',
        'title': 'Public Wi-Fi Risks',
        'icon': '📶',
        'difficulty': 'Beginner',
        'read_time': '3 min',
        'tags': ['Network', 'Privacy'],
        'overview': 'Public networks in cafes or airports are often unsecured and easy to intercept.',
        'why_matters': 'Hackers can use "Man-in-the-Middle" attacks to read your traffic on open Wi-Fi.',
        'examples': [
            'Evil Twin: A fake Wi-Fi hotspot named similarly to a legit one.',
            'Packet Sniffing: Capturing unencrypted data over the air.'
        ],
        'prevention': [
            'Avoid banking or shopping on public Wi-Fi.',
            'Use a VPN to encrypt your connection.',
            'Turn off "Auto-Connect" to Wi-Fi networks.',
            'Use mobile data (hotspot) instead if possible.'
        ],
        'quiz': [
            {
                'question': 'What is the safest way to use Public Wi-Fi?',
                'options': ['Use a VPN', 'Only browse Incognito', 'Turn off screen brightness'],
                'answer': 0
            }
        ]
    }
]

CASE_STUDIES = [
    {
        'title': 'WannaCry Ransomware (2017)',
        'date': 'May 2017',
        'what_happened': 'A global ransomware cryptoworm targeted computers running Microsoft Windows by exploiting the EternalBlue vulnerability.',
        'impact': 'Affected 200,000+ computers across 150 countries, damaging NHS hospitals, FedEx, and Renault.',
        'lessons': 'Importance of applying security patches immediately. The patch for EternalBlue was available months before the attack.'
    },
    {
        'title': 'Twitter Bitcoin Hack (2020)',
        'date': 'July 2020',
        'what_happened': 'Hackers used social engineering to gain access to Twitter\'s internal admin tools, compromising accounts of Elon Musk, Bill Gates, and Apple.',
        'impact': 'Scammers tweeted from verified accounts asking for Bitcoin, stealing ~$118,000. Massive reputation damage.',
        'lessons': 'Insider threats and social engineering are critical risks. Companies need strict access controls and zero-trust architecture.'
    },
    {
        'title': 'Colonial Pipeline Attack (2021)',
        'date': 'May 2021',
        'what_happened': 'DarkSide ransomware group compromised the billing system of the largest US fuel pipeline using a leaked password.',
        'impact': 'Pipeline shut down for days, causing fuel shortages and panic buying across the East Coast. Ransom of $4.4M paid.',
        'lessons': 'Critical infrastructure needs robust defense. Reused passwords without MFA are a single point of failure.'
    },
    {
        'title': 'MGM Resorts Cyberattack (2023)',
        'date': 'Sept 2023',
        'what_happened': 'Attackers used social engineering (vishing) to reset an employee\'s credentials via IT helpdesk.',
        'impact': 'Casino operations, room keys, and slot machines went offline. Estimated $100M loss.',
        'lessons': 'Helpdesk verification procedures must be hardened against social engineering.'
    }
]

GLOSSARY = {
    'Zero-day': 'A vulnerability that is unknown to the software vendor and has no patch available.',
    'Phishing': 'Sending fraudulent emails purporting to be from reputable companies to steal personal info.',
    'Malware': 'Malicious software including viruses, spyware, and ransomware.',
    'Ransomware': 'Malware that encrypts your files and demands payment for the decryption key.',
    'Encryption': 'The process of converting information into a code to prevent unauthorized access.',
    'Firewall': 'A network security system that monitors and controls incoming/outgoing traffic.',
    'Botnet': 'A network of private computers infected with malicious software and controlled as a group.',
    'Two-Factor Authentication (2FA)': 'Adding a second layer of security (like a code) beyond just a password.',
    'VPN': 'Virtual Private Network. Encrypts your internet traffic to protect privacy.',
    'Social Engineering': 'Manipulating people into performing actions or divulging confidential information.',
    'DDOS': 'Distributed Denial of Service. Flooding a server with traffic to crash it.',
    'Keylogger': 'Spyware that records every keystroke you make.',
    'Deepfake': 'Synthetic media where a person in an existing image or video is replaced with someone else\'s likeness.',
    'Trojan': 'Malware disguised as legitimate software.'
}

DAILY_TIPS = [
    "Lock your screen whenever you step away from your computer (Win+L).",
    "Don't click generic 'Invoice Attached' links unless you expect them.",
    "Cover your webcam when not in use.",
    "Update your browser regularly; updates often contain critical security patches.",
    "Use a phrase instead of a word for your password (e.g., 'Blue-Elephant-Jumps-High-22').",
    "Check your bank statements monthly for unauthorized transactions.",
    "Don't plug unknown USB drives into your computer.",
    "Turn on 'Find My Device' for your phone and laptop.",
    "Be careful what you share on social media; hackers use it for social engineering.",
    "Verify HTTPS and the padlock icon before entering credit card details."
]

CHECKLIST_ITEMS = [
    "I use a unique password for my email account.",
    "I have enabled 2FA on my primary accounts (Email, Bank, Social).",
    "My computer installs OS updates automatically.",
    "I use an antivirus/anti-malware solution.",
    "I verify the sender before clicking email links.",
    "I backup my important files regularly.",
    "I do not reuse passwords across multiple sites.",
    "I lock my device when leaving it unattended.",
    "I check app permissions on my phone.",
    "I know how to report a phishing attempt."
]

MYTHS_FACTS = [
    {
        'myth': 'I don’t have anything worth stealing.',
        'fact': 'Hackers want your identity, computing power (for botnets), or to use your email to attack your contacts.'
    },
    {
        'myth': 'My Mac/iPhone doesn’t get viruses.',
        'fact': 'While less common, malware exists for Apple devices. Phishing attacks work on any OS.'
    },
    {
        'myth': 'Incognito mode protects me from hackers.',
        'fact': 'Incognito only stops your browser from saving history. It does not hide your activity from your ISP or hackers.'
    },
    {
        'myth': 'Strong passwords don\'t need 2FA.',
        'fact': 'Even strong passwords can be stolen in a data breach. 2FA is your safety net.'
    }
]

BADGES = [
    {'id': 'novice_guardian', 'title': 'Novice Guardian', 'icon': '🛡️', 'desc': 'Completed your first lesson.'},
    {'id': 'cyber_scholar', 'title': 'Cyber Scholar', 'icon': '🎓', 'desc': 'Completed all lessons.'},
    {'id': 'fortress', 'title': 'Fortress', 'icon': '🏰', 'desc': 'Achieved "Low Risk" status on the Risk Assessment.'}
]
