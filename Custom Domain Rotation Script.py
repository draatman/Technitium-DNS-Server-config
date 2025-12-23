#!/usr/bin/env python3
# rotate-health-domains.py
import requests
import datetime

# List of domains to rotate through
DOMAINS = [
    "example.com",
    "example.net", 
    "example.org",
    "ietf.org",
    "w3.org",
    "wikipedia.org"
]

def get_todays_domain():
    """Select domain based on day of week and hour"""
    now = datetime.datetime.now()
    
    # Simple rotation: domain index based on day and hour
    # 7 days × 3 checks/day = 21 positions, cycle through 6 domains
    day_of_year = now.timetuple().tm_yday
    hour_slot = now.hour // 8  # 0, 1, or 2 (for 8-hour intervals)
    
    position = (day_of_year * 3 + hour_slot) % len(DOMAINS)
    return DOMAINS[position]

def update_technitium(domain):
    """Update Technitium with today's health check domain"""
    config = {
        "healthCheckDomain": domain,
        "healthCheckInterval": 28800,
        "healthCheckMinimumSuccess": 1
    }
    
    for server in ['technitium-primary:5380', 'technitium-secondary:5380']:
        try:
            response = requests.post(f"http://{server}/api/settings/dns", 
                                   json=config, timeout=10)
            print(f"Updated {server} to check {domain}")
        except Exception as e:
            print(f"Failed to update {server}: {e}")

if __name__ == "__main__":
    today_domain = get_todays_domain()
    print(f"Selected domain for checking: {today_domain}")
    update_technitium(today_domain)
