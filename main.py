from bs4 import BeautifulSoup
import requests
from pprint import pprint
import ProfileFinder as pf
import fileinput

if __name__ == '__main__':
    #s = input('')
    #nameList = s.split(' ')
    nameList = []
    for names in fileinput.input(files="input.txt"):
        names = names.strip()
        nameList.append(names)

    f = open('output.txt', 'w')
    f.write("")
    f.close()
    for username in nameList:
        pf.FindProfile(username)
