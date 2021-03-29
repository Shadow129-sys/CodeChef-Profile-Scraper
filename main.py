import ProfileFinder as pf
import fileinput

if __name__ == '__main__':
    nameList = []
    
    #for extracting the usernames from each line of the "input.txt"
    for names in fileinput.input(files="input.txt"):
        names = names.strip()
        nameList.append(names)

    #clearing out the "output.txt" file 
    f = open('output.txt', 'w')
    f.write("")
    f.close()
    
    #sending the usernames one by one to extract information
    for username in nameList:
        pf.FindProfile(username)
