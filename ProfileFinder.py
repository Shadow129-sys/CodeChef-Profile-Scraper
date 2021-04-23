from bs4 import BeautifulSoup
import requests
from pprint import pprint
import time
 
#To store color code for different stars
coderDiv = ["Grey", "Green", "Blue", "Violet", "Yellow", "Orange", "Red"]

#Searches for information in the user's profile page
def FindProfile(username: str):

    #For storing the final search result
    description = ""

    try:
        url = "https://www.codechef.com/users/" + username
        website_html = requests.get(url).text
        soup = BeautifulSoup(website_html, 'lxml')

        ProfileDetails = soup.find('section', class_="user-details")
        moreinfo = ProfileDetails.find_all('li')

        for details in moreinfo:

            infoTitle = details.label.text[:-1]
            if infoTitle == "Teams List":
                break

            if infoTitle == "Username":
                description += infoTitle + " : " + username + '\n'
                continue

            infoValue = details.span.text.strip()
            description += infoTitle + " : " + infoValue + '\n'

        CurrentRating = soup.find('div', class_="rating-number").text.strip()
        CurrentRatingNumber = int(CurrentRating)
        currentStars = FindStars(CurrentRatingNumber)
        CurrentCoderType = coderDiv[currentStars - 1] + " coder"

        HeighestRating = soup.find(
            'div', class_="rating-header text-center").small.text
        HeighestRating = HeighestRating.split(' ')[-1][:-1]
        HeighestRatingNumber = int(HeighestRating)
        HeighestStars = FindStars(HeighestRatingNumber)
        HeighestCoderType = coderDiv[HeighestStars - 1] + " coder"

        description += f"Current : {CurrentCoderType} {currentStars}star {CurrentRatingNumber} | Heighest : {HeighestCoderType} {HeighestStars}star {HeighestRatingNumber}\n"

        GCRanks = soup.find('div', class_='rating-ranks').ul.find_all('li')
        GlobalRank = GCRanks[0].text.split('\n')
        description += f"{GlobalRank[2].strip()} : {GlobalRank[1].strip()} | "

        CountryRank = GCRanks[1].text.split('\n')
        description += f"{CountryRank[2].strip()} : {CountryRank[1].strip()}\n"

        RankStats = soup.find('div', class_='rank-stats')
        LastContestInfo = RankStats.find('div', class_='contest-name')
        ContestName = LastContestInfo.a.text.strip()

        if ContestName == 'None':
            description += "Last Rated Contest : " + ContestName + '\n'
        else:
            ContestLink = LastContestInfo.a['href']
            LastRatingInfo = RankStats.find('div', class_='rating-container')
            RatingChanged = LastRatingInfo.find('span').text.strip()

            description += "Last Rated Contest : " + ContestName + '\n'
            description += "Rating Changed : " + RatingChanged + '\n'
            description += "Link : " + ContestLink + '\n'

        SolvedProblemsTable = soup.find(
            'section', {'class': 'rating-data-section problems-solved'})
        FullySolved, PartiallySolved = SolvedProblemsTable.find_all('h5')
        FullySolved = FullySolved.text.split('(')[-1][:-1]
        PartiallySolved = PartiallySolved.text.split('(')[-1][:-1]
        description += f"Fully Solved : {FullySolved} | Partially Solved : {PartiallySolved}\n"

        ContestProblems = {"Practice": 0}
        ProblemsSolved = SolvedProblemsTable.find_all('article')
        MaxProblemSolved = -1
        MaxProblemSolvedContest = ""

        Contests = ProblemsSolved[0].find_all('p')
        for contest in Contests:
            contestName = contest.strong.text[:-1]
            if(contestName == "Practice"):
                ContestProblems["Practice"] += len(contest.span.find_all('a'))
                continue

            ContestProblems[contestName] = len(contest.span.find_all('a'))

            if(ContestProblems[contestName] >= MaxProblemSolved):
                MaxProblemSolved = ContestProblems[contestName]
                MaxProblemSolvedContest = contestName

            #print(contestName + f"  {ContestProblems[contestName]}")

        if("Practice" in ContestProblems.keys()):
            description += f"Practice Problems : {ContestProblems['Practice']}\n"

        if((len(Contests) > 1) or (len(Contests) == 1 and ("Practice" in ContestProblems.keys()))):
            description += f"Most Problem Solved in Contests : {MaxProblemSolved}\n"
            description += f"Contests Code : {MaxProblemSolvedContest}\n"
            description += f"Link : https://www.codechef.com/{MaxProblemSolvedContest}\n"

        flag = False
        try:
            Contests = ProblemsSolved[1].find_all('p')
            flag = True
        except:
            pass

        if(flag):
            for contest in Contests:
                contestName = contest.strong.text[:-1]
                ContestProblems[contestName] = 1

        ContestsParticipated = 0
        if("Practice" in ContestProblems.keys()):
            ContestsParticipated = len(ContestProblems.keys()) - 1
        else:
            ContestsParticipated = len(ContestProblems.keys())
        description += f"Contests Participated : {ContestsParticipated}\n"

        if("Practice" in ContestProblems.keys()):
            del ContestProblems["Practice"]

        description += "Contest List : " + \
            str(list(ContestProblems.keys())) + '\n'

    except:
        description = f"Username '{username}' dosen't exists\n"

    description += 100*"-" + '\n'
    
    #writes the info of the user into the output file
    f = open('output.txt', 'a')
    f.write(description)
    f.close()


#For finding out the stars from rating of the user
def FindStars(rating: str):

    rating = int(rating)

    if(rating >= 2500):
        return 7
    if(rating < 2500 and rating >= 2200):
        return 6
    if(rating < 2200 and rating >= 2000):
        return 5
    if(rating < 2000 and rating >= 1800):
        return 4
    if(rating < 1800 and rating >= 1600):
        return 3
    if(rating < 1600 and rating >= 1400):
        return 2
    else:
        return 1
