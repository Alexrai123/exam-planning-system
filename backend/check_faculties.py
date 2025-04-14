import requests

def check_faculties():
    url = "https://orar.usv.ro/orar/vizualizare/data/facultati.php?json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"Successfully fetched {len(data)} faculties")
            for faculty in data:
                print(f"ID: {faculty.get('id', 'N/A')}, Name: {faculty.get('name', 'N/A')}, Short Name: {faculty.get('shortName', 'N/A')}")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    check_faculties()
