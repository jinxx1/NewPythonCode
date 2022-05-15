import requests

url = "https://94i888.com/api.php?type=video&category=1&page=1"
brow = requests.get(url=url)
print(brow.text)