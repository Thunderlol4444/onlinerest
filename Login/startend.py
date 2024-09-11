import requests

if __name__ == '__main__':
    print(requests.get('http://localhost:8000/hello').content)
    print(requests.get('http://localhost:8000/shutdown').content)