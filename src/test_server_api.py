import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import app

client = app.test_client()

# Test 1: GET /
res_home = client.get('/')
print(f"GET / -> Status: {res_home.status_code}, Length: {len(res_home.data)}")
assert res_home.status_code == 200
assert b'min="2006"' in res_home.data
assert b'max="2026"' in res_home.data
assert b'tab-studio' in res_home.data
assert b'tab-bulk' in res_home.data

# Test 2: POST /api/predict with 2006 vehicle
payload_2006 = {
    'brand': 'Maruti Suzuki',
    'model': 'Swift',
    'make_year': 2006,
    'mileage_kmpl': 18.5,
    'engine_cc': 1298,
    'fuel_type': 'Petrol',
    'transmission': 'Manual',
    'color': 'Silver',
    'owner_count': 3,
    'service_history': 'Partial',
    'accidents_reported': 1,
    'insurance_valid': 'No'
}
res_pred1 = client.post('/api/predict', json=payload_2006)
print(f"POST /api/predict (2006 Swift) -> Status: {res_pred1.status_code}")
data1 = res_pred1.get_json()
assert res_pred1.status_code == 200
assert data1['success'] is True
print("Single prediction successful:", data1['price_lakh_str'])

# Test 3: POST /api/predict_bulk
bulk_payload = [
    payload_2006,
    {
        'brand': 'Toyota',
        'model': 'Fortuner',
        'make_year': 2023,
        'mileage_kmpl': 14.2,
        'engine_cc': 2755,
        'fuel_type': 'Diesel',
        'transmission': 'Automatic',
        'color': 'White',
        'owner_count': 1,
        'service_history': 'Authorized Dealer',
        'accidents_reported': 0,
        'insurance_valid': 'Yes'
    }
]
res_bulk = client.post('/api/predict_bulk', json={'cars': bulk_payload})
print(f"POST /api/predict_bulk -> Status: {res_bulk.status_code}")
data_bulk = res_bulk.get_json()
assert res_bulk.status_code == 200
assert data_bulk['success'] is True
assert data_bulk['count'] == 2
print(f"Bulk prediction successful: {data_bulk['count']} cars, total: ₹ {data_bulk['total_lakh']} Lakh")

print("\nALL API AND FRONTEND CHECKS PASSED WITH 100% SUCCESS!")
