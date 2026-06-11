import urllib.request

url = "https://raw.githubusercontent.com/cmusphinx/cmudict/master/cmudict.dict"
urllib.request.urlretrieve(url, "cmu_raw.txt")
print("Done")