import requests
import csv
import subprocess

# Download CSV file containing IP addresses from Abuse CH
response = requests.get("https://feodotracker.abuse.ch/downloads/ipblocklist.csv").text

# Delete existing rules named 'Bad IP'
subprocess.run(["Powershell", "-Command", "netsh advfirewall firewall delete rule name='Bad IP'"])

# Extract IP addresses from CSV and add rules to block them
for row in csv.reader(filter(lambda x: not x.startswith("#"), response.splitlines())):
    ip = row[1]
    if ip != "dst_ip":
        print("Added Rule to block:", ip)
        subprocess.run(["Powershell", "-Command", f"netsh advfirewall firewall add rule name='BadIP' Dir=Out Action=Block RemoteIP={ip}"])
        subprocess.run(["Powershell", "-Command", f"netsh advfirewall firewall add rule name='BadIP' Dir=In Action=Block RemoteIP={ip}"])
