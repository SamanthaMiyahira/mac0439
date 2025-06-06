import requests

url = 'http://localhost:8000/api/confirmar-saida/'

data = {
    "qrcode": "https://example.com/qrcode123", 
    "placa": "YZA5B67"    
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())
