import urllib.request
url = "https://raw.githubusercontent.com/openlanguageprofiles/olp-en-cefrj/master/cefrj-vocabulary-profile-1.5.csv"
urllib.request.urlretrieve(url, "oxford_raw.csv")
print("Done")