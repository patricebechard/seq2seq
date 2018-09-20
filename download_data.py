from urllib.request import urlretrieve
import tarfile
import os

# using europarl datasets : http://www.statmt.org/europarl/

DATADIR = 'data/'

file_url = 'http://www.statmt.org/europarl/v7/fr-en.tgz'
file_name = 'fr-en.tgz'

def download_data():

	if not os.path.exists(DATADIR):
		os.makedirs(DATADIR)

	print("Downloading file...")
	urlretrieve(file_url, DATADIR + file_name)

	print("Unzipping file...")
	tar = tarfile.open(DATADIR + file_name, "r:gz")
	tar.extractall(path=DATADIR)
	tar.close()

	os.remove(DATADIR + file_name)

if __name__ == "__main__":

	download_data()