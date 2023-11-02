import requests


def json_health_check():
    public_health = "http://localhost:3000/health"
    admin_health = "http://localhost:3001/health"

    try:
        public_response = requests.get(public_health)
        admin_response = requests.get(admin_health)

        if public_response.status_code == 200:
            public_data = public_response.json()
            if 'status' in public_data and public_data['status'] == 'success':
                if public_data['results'][0]['passed'] is True:
                    print("Public app JSON response is healthy")
            else:
                print("Public app JSON response is not healthy")
        else:
            print(f"Public app HTTP request failed with status code: {public_response.status_code}")

        if admin_response.status_code == 200:
            admin_data = admin_response.json()
            if 'status' in admin_data and admin_data['status'] == 'success':
                if admin_data['results'][0]['passed'] is True:
                    print("Admin app JSON response is healthy")
            else:
                print("Admin app JSON response is not healthy")
        else:
            print(f"Admin app HTTP request failed with status code: {public_response.status_code}")

    except requests.exceptions.RequestException as e:
        print("Error: could not access health page")

json_health_check()