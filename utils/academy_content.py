# academy_content.py

LEARNING_PATHS = {
    'red': {
        'id': 'red',
        'title': 'Red Teaming (Offensive Security)',
        'icon': '🔴',
        'description': 'Simulate cyber attacks to find vulnerabilities before malicious actors do.',
        'color': 'danger',
        'modules': [
            {
                'title': 'Networking Basics',
                'desc': 'Master TCP/IP, OSI Model, DNS, HTTP/HTTPS, and Subnetting.',
                'time': '10 Hours',
                'difficulty': 'Beginner',
                'resources': ['CompTIA Network+', 'Cisco Packet Tracer'],
                'project': 'Build a localized network with 3 subnets.'
            },
            {
                'title': 'Linux & Scripting',
                'desc': 'Command line proficiency (Bash), Python automation, and tool building.',
                'time': '15 Hours',
                'difficulty': 'Beginner',
                'resources': ['OverTheWire Bandit', 'Automate the Boring Stuff with Python'],
                'project': 'Write a Bash script to automate Nmap scans.'
            },
            {
                'title': 'Vulnerability Assessment',
                'desc': 'Scanning with Nmap, identifying weak configs with Nessus/OpenVAS.',
                'time': '12 Hours',
                'difficulty': 'Intermediate',
                'resources': ['Nessus Essentials', 'VulnHub Machines'],
                'project': 'Scan a target VM and report 5 vulnerabilities.'
            },
            {
                'title': 'Exploitation Techniques',
                'desc': 'Metasploit Framework, Burp Suite, SQL Injection, XSS, Buffer Overflows.',
                'time': '25 Hours',
                'difficulty': 'Advanced',
                'resources': ['PortSwigger Web Security Academy', 'HackTheBox'],
                'project': 'Root a "Easy" box on HackTheBox.'
            },
            {
                'title': 'Privilege Escalation',
                'desc': 'Linux SUID/Sudo abuse, Windows Token manipulation, Kernel exploits.',
                'time': '20 Hours',
                'difficulty': 'Advanced',
                'resources': ['Tib3rius PrivEsc Courses', 'GTFOBins'],
                'project': 'Escalate from user to root on a practice Linux VM.'
            }
        ]
    },
    'blue': {
        'id': 'blue',
        'title': 'Blue Teaming (Defensive Security)',
        'icon': '🔵',
        'description': 'Defend organizations by monitoring, detecting, and responding to threats.',
        'color': 'info',
        'modules': [
            {
                'title': 'Network Defense',
                'desc': 'Firewalls, IDS/IPS (Snort/Suricata), VPNs, and Access Control Lists.',
                'time': '12 Hours',
                'difficulty': 'Beginner',
                'resources': ['Cisco CyberOps', 'Pfsense Labs'],
                'project': 'Configure a firewall to block specific traffic.'
            },
            {
                'title': 'SIEM & Log Analysis',
                'desc': 'Splunk, ELK Stack, Reading Syslogs, Windows Event Forwarding.',
                'time': '18 Hours',
                'difficulty': 'Intermediate',
                'resources': ['Splunk Fundamentals', 'LetsDefend'],
                'project': 'Set up a Splunk instance and ingest Windows logs.'
            },
            {
                'title': 'Incident Response',
                'desc': 'NIST Framework, Containment, Eradication, Recovery procedures.',
                'time': '15 Hours',
                'difficulty': 'Intermediate',
                'resources': ['NIST SP 800-61', 'Black Hills Infosec'],
                'project': 'Draft an Incident Response Plan for Ransomware.'
            },
            {
                'title': 'Digital Forensics',
                'desc': 'Analyzing disk images (Autopsy), Volatility for memory looking for artifacts.',
                'time': '20 Hours',
                'difficulty': 'Advanced',
                'resources': ['Autopsy User Guide', 'SANS DFIR Posters'],
                'project': 'Analyze a memory dump to find a hidden process.'
            },
            {
                'title': 'Threat Intelligence',
                'desc': 'Understanding APTs, IoCs, TTPs, and the MITRE ATT&CK Framework.',
                'time': '10 Hours',
                'difficulty': 'Advanced',
                'resources': ['MITRE ATT&CK', 'AlienVault OTX'],
                'project': 'Map a known APT group to MITRE techniques.'
            }
        ]
    },
    'purple': {
        'id': 'purple',
        'title': 'Purple Teaming',
        'icon': '🟣',
        'description': 'Bridge the gap between Red and Blue teams to improve overall security.',
        'color': 'primary', # Using primary (purple-ish in theme) or custom CSS
        'modules': [
            {
                'title': 'Adversary Emulation',
                'desc': 'Mimicking real-world threat actors to test defenses.',
                'time': '15 Hours',
                'difficulty': 'Intermediate',
                'resources': ['Atomic Red Team', 'Caldera'],
                'project': 'Run an Atomic Red Team test and verify detection.'
            },
            {
                'title': 'Detection Engineering',
                'desc': 'Writing detection rules (Sigma, YARA, Snort) based on attacks.',
                'time': '20 Hours',
                'difficulty': 'Advanced',
                'resources': ['Sigma HQ', 'YARA documentation'],
                'project': 'Write a Sigma rule to detect a specific PowerShell command.'
            }
        ]
    },
    'soc': {
        'id': 'soc',
        'title': 'SOC Analyst',
        'icon': '🛡️',
        'description': 'The frontline defenders monitoring security operations centers.',
        'color': 'success',
        'modules': [
            {
                'title': 'Log Analysis Fundamentals',
                'desc': 'Understanding Syslogs, Windows Events, and identifying anomalies.',
                'time': '10 Hours',
                'difficulty': 'Beginner',
                'resources': ['Blue Team Labs Online', 'TryHackMe SOC Path'],
                'project': 'Analyze a web server log to find a SQL injection attempt.'
            },
            {
                'title': 'Phishing Analysis',
                'desc': 'Email header analysis, URL rep checks, Sandbox execution.',
                'time': '8 Hours',
                'difficulty': 'Intermediate',
                'resources': ['PhishTool', 'Any.Run'],
                'project': 'Analyze a sample phishing email and extract IoCs.'
            },
            {
                'title': 'Ticket Handling & Triage',
                'desc': 'Severity classification, escalation matrices, and reporting.',
                'time': '5 Hours',
                'difficulty': 'Beginner',
                'resources': ['TheHive Project', 'ServiceNow Security Ops'],
                'project': 'Simulate a shift handling 5 alerts.'
            }
        ]
    }
}

CAREER_ROLES = [
    {
        'id': 'soc_analyst',
        'title': 'SOC Analyst (L1/L2)',
        'level': 'Entry Level',
        'salary': '$60k - $90k',
        'desc': 'The first line of defense. Monitors alerts, investigates suspicious activity, and triages incidents.',
        'color': 'primary',
        'skills': ['Linux/Windows OS', 'Networking (TCP/IP)', 'SIEM (Splunk/Sentinel)', 'Phishing Analysis'],
        'tools': ['Splunk', 'Wireshark', 'TheHive', 'VirusTotal'],
        'certs': ['CompTIA Security+', 'CySA+', 'BTL1'],
        'progression': ['Incident Responder', 'Threat Hunter', 'Security Engineer'],
        'tips': [
            'Build a home lab with ELK Stack.',
            'Practice analyzing PCAP files on traffic analysis sites.',
            'Learn to explain "false positives" vs "true positives".'
        ]
    },
    {
        'id': 'pentester',
        'title': 'Penetration Tester',
        'level': 'Mid-Level',
        'salary': '$90k - $130k',
        'desc': 'Ethical hackers authorized to test systems for weaknesses using real-world attack techniques.',
        'color': 'danger',
        'skills': ['Python/Bash Scripting', 'Web App Security', 'Active Directory', 'Network Pivoting'],
        'tools': ['Burp Suite', 'Metasploit', 'Nmap', 'BloodHound'],
        'certs': ['eJPT', 'OSCP', 'CEH (Practical)', 'PNPT'],
        'progression': ['Red Team Lead', 'Security Consultant', 'CISO'],
        'tips': [
            'Rank up on HackTheBox or TryHackMe.',
            'Write writeups for machines you solve.',
            'Understand OWASP Top 10 vulnerabilities deeply.'
        ]
    },
    {
        'id': 'security_engineer',
        'title': 'Security Engineer',
        'level': 'Mid-Senior',
        'salary': '$110k - $160k',
        'desc': 'Builds, maintains, and hardens security infrastructure like firewalls, IDS/IPS, and cloud controls.',
        'color': 'success',
        'skills': ['Cloud Security (AWS/Azure)', 'IaC (Terraform)', 'Python', 'DevSecOps'],
        'tools': ['Ansible', 'Terraform', 'CrowdStrike', 'Palo Alto Firewalls'],
        'certs': ['CISSP', 'AWS Security Specialty', 'CCSP'],
        'progression': ['Security Architect', 'Head of Infrastructure', 'CISO'],
        'tips': [
            'Learn Infrastructure as Code (IaC).',
            'Automate repetitive security tasks with Python.',
            'Understand zero-trust architecture principles.'
        ]
    },
    {
        'id': 'dfir',
        'title': 'DFIR Specialist',
        'level': 'Senior',
        'salary': '$100k - $150k',
        'desc': 'Digital Forensics and Incident Response. Investigates breaches to determine the "who, what, where, and how".',
        'color': 'info',
        'skills': ['Disk Forensics', 'Memory Forensics', 'Malware Analysis', 'Legal Chain of Custody'],
        'tools': ['Autopsy', 'Volatility', 'FTK Imager', 'YARA'],
        'certs': ['GCFA', 'GNFA', 'EnCE'],
        'progression': ['DFIR Lead', 'Director of Incident Response'],
        'tips': [
            'Participate in DFIR CTFs.',
            'Learn to accept that you won\'t catch everything.',
            'Master the art of writing clear, legal-ready reports.'
        ]
    },
    {
        'id': 'ciso',
        'title': 'Chief Information Security Officer',
        'level': 'Executive',
        'salary': '$180k - $300k+',
        'desc': 'Executive responsible for the entire organization\'s security strategy, budget, and compliance.',
        'color': 'warning',
        'skills': ['Risk Management', 'Compliance (GDPR/HIPAA)', 'Budgeting', 'Leadership'],
        'tools': ['GRC Tools', 'Excel', 'Board Presentations'],
        'certs': ['CISSP', 'CISM', 'CISA'],
        'progression': ['CIO', 'CRO (Chief Risk Officer)'],
        'tips': [
            'Focus on business alignment, not just technical controls.',
            'Learn to speak the language of the board of directors.',
            'Build a strong professional network.'
        ]
    }
]
