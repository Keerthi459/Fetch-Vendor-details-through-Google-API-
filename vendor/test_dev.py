import requests
from config import API_KEY

params = {'address': 'Madurai, Tamil Nadu', 'key': API_KEY}
res = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params).json()
print("FULL RESPONSE:")
print(res)
