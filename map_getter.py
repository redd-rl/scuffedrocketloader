import requests
def get_map(mapPageUrl):
    request = requests.get(mapPageUrl)
    with open("downloaded.zip", "wb") as handle:
        handle.write(request.content)