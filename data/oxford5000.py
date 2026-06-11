import urllib.request
url = "https://raw.githubusercontent.com/nalgeon/words/main/data/oxford-5k.csv"
urllib.request.urlretrieve(url, "oxford5k_raw.csv")
print("Done")