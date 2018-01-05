#!/usr/bin/env python
# Version 1.0.1
# Version Updates:
#  - resize horizontally to fit different resolutions

# to do
# - check if name is already in CSV
# make look nice
# on view profile, view past games and graph of past ranks/grade
# also view longest win streak etc.


__author__ = 'vignesh'
# playerinfo --> firstname, lastname, form, rank, wins, losses, draws, grade, attendance
# playerdata --> fname1, lname1, oldrank1, oldgrade1, result, fname2, lname2, oldrank2, oldgrade2, date
from tkinter import *
from tkinter import messagebox
from operator import itemgetter
import csv
import datetime

recordWindow = None
now = datetime.datetime.now()


def window_record():
    # opens a new window if the record button is clicked
    global  recordWindow
    recordWindow = Toplevel(root)
    # produces all the buttons and labels
    recordTitle = Label(recordWindow, text="Record Game", font="Verdana 60 bold", pady='10')
    recordTitle.grid(row=0, columnspan=10)
    recordInfoLabel = Label(recordWindow, text='Enter the ranks of the two players, does not matter which order.')
    recordInfoLabel.grid(row=1, columnspan=10)
    recordInfoLabel2 = Label(recordWindow, text='Click whether the CHALLENGE was a draw, successful or a fail.')
    recordInfoLabel2.grid(row=2, columnspan=10)
    player1Label = Label(recordWindow, text='Player one rank', font="Verdana 20", pady='10')
    player1Label.grid(row=4, column=0, columnspan=4)
    player2Label = Label(recordWindow, text='Player two rank', font="Verdana 20", pady='10')
    player2Label.grid(row=4, column=6, columnspan=4)
    player1Entry = Entry(recordWindow)
    player1Entry.grid(row=5, column=0, columnspan=4)
    player2Entry = Entry(recordWindow)
    player2Entry.grid(row=5, column=6, columnspan=4)
    successButton = Button(recordWindow, text='Success', font='Verdana 20 bold', pady='10',
                           command=lambda: check_challenge('success', player1Entry.get(), player2Entry.get()))
    successButton.grid(row=6, column=0, columnspan=3)
    drawButton = Button(recordWindow, text='Draw', font='Verdana 20 bold', pady='10',
                        command=lambda: check_challenge('draw', player1Entry.get(), player2Entry.get()))
    drawButton.grid(row=6, column=4, columnspan=2)
    failButton = Button(recordWindow, text='Fail', font='Verdana 20 bold', pady='10',
                        command=lambda: check_challenge('fail', player1Entry.get(), player2Entry.get()))
    failButton.grid(row=6, column=7, columnspan=3)


def check_challenge(result, rank1, rank2):
    rank1 = int(rank1)
    rank2 = int(rank2)
    winner = 'none'
    loser = 'none'
    # looks up the name of the corresponding players
    for name in ladder_data_list:
        if int(name[0]) == rank1:
            winner = name[1]
        if int(name[0]) == rank2:
            loser = name[1]
    # validation to check those ranks are actually signed in
    if winner == 'none' or loser == 'none':
        display_message('none', 'none', 'none')
        return None
    if result == 'success':
        # validates the names the right way round
        if rank1 < rank2:
            temp = winner
            winner = loser
            loser = temp
        display_message('success', winner, loser)
    elif result == 'draw':
        display_message('draw', winner, loser)
    elif result == 'fail':
        # also validates the names the right way round
        if rank1 > rank2:
            temp = winner
            winner = loser
            loser = temp
        display_message('fail', winner, loser)

# module for deciding what to do with the result
def display_message(result, winner, loser):
    global recordWindow
    # removes all the previous labels on the grid
    for label in recordWindow.grid_slaves():
        if int(label.grid_info()["row"]) > 6:
            label.grid_remove()
    # depending on if successful, fail or draw displays appropriate message
    # if the no button is clicked, the message is cleared
    # if the yes button is clicked, statistics are updated
    if result == 'success':
        resultMessage = 'Are you sure ' + winner + ' beat ' + loser
        checkResultLabel = Label(recordWindow, text=resultMessage, pady='10')
        checkResultLabel.grid(row=8, columnspan=10)
        resultYesButton = Button(recordWindow, text='Yes', font='Verdana 15 bold',
                                 command=lambda: update_stats('success', winner, loser))
        resultYesButton.grid(row=9, column=2, columnspan=3)
        resultNoButton = Button(recordWindow, text='No', font='Verdana 15 bold',
                                command=lambda: display_message('clear', 'none', 'none'))
        resultNoButton.grid(row=9, column=7, columnspan=2)
    elif result == 'draw':
        resultMessage = 'Are you sure ' + winner + ' drew against ' + loser
        checkResultLabel = Label(recordWindow, text=resultMessage, pady='10')
        checkResultLabel.grid(row=8, columnspan=10)
        resultYesButton = Button(recordWindow, text='Yes', font='Verdana 15 bold',
                                 command=lambda: update_stats('draw', winner, loser))
        resultYesButton.grid(row=9, column=2, columnspan=3)
        resultNoButton = Button(recordWindow, text='No', font='Verdana 15 bold',
                                command=lambda: display_message('clear', 'none', 'none'))
        resultNoButton.grid(row=9, column=7, columnspan=2)
    elif result == 'fail':
        resultMessage = 'Are you sure ' + winner + ' beat ' + loser
        checkResultLabel = Label(recordWindow, text=resultMessage, pady='10')
        checkResultLabel.grid(row=8, columnspan=10)
        resultYesButton = Button(recordWindow, text='Yes', font='Verdana 15 bold',
                                 command=lambda: update_stats('fail', winner, loser))
        resultYesButton.grid(row=9, column=2, columnspan=3)
        resultNoButton = Button(recordWindow, text='No', font='Verdana 15 bold',
                                command=lambda: display_message('clear', 'none', 'none'))
        resultNoButton.grid(row=9, column=7, columnspan=2)
    # if 'no' is clicked when asked 'are you sure' it returns nothing
    elif result == 'clear':
        return None
    # if the player can't be found, an error message is returned
    else:
        messagebox.showerror(message='One or both of those players have not signed in')


root = Tk()
# resizing fixing
Grid.columnconfigure(root, 0, weight=1)
Grid.rowconfigure(root, 0, weight=1)
# initialise arrays etc.
sign_in_data_list = []
ladder_data_list = []
sign_out_button_list = ['none'] * 1000
ladderCounter = 3
homeImage = PhotoImage(file="home_button.gif")

# reading a file
readFile = open('playerinfo.csv')
reader = csv.reader(readFile)

# converting csv to lists for the chess database / chessdb / player info
with open('playerinfo.csv', 'rt') as f:
    csvToList = csv.reader(f)
    playerInfo = list(csvToList)
    playerInfo = [[s.strip() for s in inner] for inner in playerInfo]
    random_rank_counter = 1
    for rank in playerInfo:
        rank[3] = random_rank_counter
        random_rank_counter += 1


# converting csv to lists for the match history
with open('matchhistory.csv', 'rt') as g:
    csvToList2 = csv.reader(g)
    playerData = list(csvToList2)
    playerData = [[s.strip() for s in inner] for inner in playerData]


# function which gets called whenever a frame (screen) needs to be changed
def raise_frame(frame):
    # essentially if home button is pressed
    # refreshes the page
    if frame == mainFrame:
        title = Label(mainFrame, text="Wilson's School Chess Club", font="Verdana 60 bold", pady='10')
        title.grid(columnspan=21, sticky='W')
        sort_names_ladder()
    frame.tkraise()

# creates 'frames' for each screen
# then puts them onto a grid
mainFrame = Frame(root)
mainFrame.grid(row=0, column=0, sticky='news')
signInFrame = Frame(root)
signInFrame.grid(row=0, column=0, sticky='news')
registerFrame = Frame(root)
registerFrame.grid(row=0, column=0, sticky='news')
viewLadderFrame = Frame(root)
viewLadderFrame.grid(row=0, column=0, sticky='news')
viewProfileFrame = Frame(root)
viewProfileFrame.grid(row=0, column=0, sticky='news')
# array to store all frame names
frame_names = [mainFrame, signInFrame, registerFrame, viewLadderFrame, viewProfileFrame]
# resizing issue fix for all frames
# for q in frame_names:
#    Grid.columnconfigure(q, 0, weight=1)
#    Grid.rowconfigure(q, 0, weight=1)

# checks if player hasn't signed in
def check_attendance():
    for player in playerInfo:
        # finds the how many days since last sign in
        todaydate = now.strftime("%Y-%m-%d")
        lastdate = player[9]
        todaydate = datetime.datetime.strptime(todaydate, "%Y-%m-%d")
        lastdate = datetime.datetime.strptime(lastdate, "%Y-%m-%d")
        difference = (todaydate-lastdate).days
        # if it's been 1-4 weeks then move down 10 places
        # if it's been over a month, then move down to the bottom
        if int(player[8]) == 0:
            if difference > 7:
                attendance_reorder_list(player)
                player[8] = 1
        elif int(player[8]) == 1:
            if difference > 14:
                attendance_reorder_list(player)
                player[8] = 2
        elif int(player[8]) == 2:
            if difference > 21:
                attendance_reorder_list(player)
                player[8] = 3
        elif int(player[8]) == 3:
            if difference > 28:
                playerInfo.insert(len(playerInfo)-1, playerInfo.pop(playerInfo.index(player)))
                # reranks the records
                anotherCounter = 1
                for j in playerInfo:
                    j[3] = anotherCounter
                    anotherCounter += 1
                player[8] = 4


def attendance_reorder_list(player):
    # moves the records around
    tempAttendancerecord = player
    playerpos = playerInfo.index(tempAttendancerecord)
    if playerpos + 11 < len(playerInfo) - 1:
        for i in range(playerpos, playerpos + 11):
            playerInfo[i] = playerInfo[i+1]
        playerInfo[playerpos+10] = tempAttendancerecord
        # reranks the records
        anotherCounter = 1
        for j in playerInfo:
            j[3] = anotherCounter
            anotherCounter += 1
    else:
        playerInfo.insert(len(playerInfo)-1, playerInfo.pop(playerInfo.index(player)))
        # reranks the records
        anotherCounter = 1
        for j in playerInfo:
            j[3] = anotherCounter
            anotherCounter += 1


# updates the stats of the players and records the games
def update_stats(result, winner, loser):
    global recordWindow
    listcounterwinner = 0
    listcounterloser = 0
    winneri = 0
    loseri = 0
    winner = winner.split()
    loser = loser.split()
    # finds the location of the players in the main list
    for name in playerInfo:
        if name[0] == winner[0] and name[1] == winner[1]:
            winneri = listcounterwinner
        if name[0] == loser[0] and name[1] == loser[1]:
            loseri = listcounterloser
        listcounterwinner += 1
        listcounterloser += 1
    # increase number of wins/losses/draws of each player
    if result == 'success':
        internal_grade_calculation(winneri, loseri, 'success')
        store_match(winneri, loseri, result)
        playerInfo[winneri][4] = int(playerInfo[winneri][4]) + 1
        playerInfo[loseri][5] = int(playerInfo[loseri][5]) + 1
        reorder_list(winneri, loseri)
    elif result == 'fail':
        internal_grade_calculation(winneri, loseri, 'fail')
        store_match(winneri, loseri, result)
        playerInfo[winneri][4] = int(playerInfo[winneri][4]) + 1
        playerInfo[loseri][5] = int(playerInfo[loseri][5]) + 1
    elif result == 'draw':
        internal_grade_calculation(winneri, loseri, 'draw')
        store_match(winneri, loseri, result)
        playerInfo[winneri][6] = int(playerInfo[winneri][6]) + 1
        playerInfo[loseri][6] = int(playerInfo[loseri][6]) + 1
    recordWindow.destroy()
    raise_frame(mainFrame)


# changes the internal grade
def internal_grade_calculation(winnerpos, loserpos, result):
    # assign the grades of two players to these variables
    winnergrade = int(playerInfo[winnerpos][7])
    losergrade = int(playerInfo[loserpos][7])
    # algorithm for changing grade depending on result
    # exception for draws:
    if winnergrade > losergrade and result == 'draw':
        winnergrade = int(playerInfo[loserpos][7])
        losergrade = int(playerInfo[winnerpos][7])
    elif result == 'draw' and winnergrade == losergrade:
        return None

    if winnergrade <= losergrade:
        winnergrade2 = int((losergrade-winnergrade)/5) + 4 + winnergrade
        losergrade -= int((losergrade-winnergrade)/5) + 4
        winnergrade = winnergrade2
    elif winnergrade > losergrade:
        winnergrade2 = int(4/(0.1*(winnergrade-losergrade)+1)) + winnergrade
        losergrade -= int(4/(0.1*(winnergrade-losergrade)+1))
        winnergrade = winnergrade2
    # change the grades in the list
    playerInfo[winnerpos][7] = winnergrade
    playerInfo[loserpos][7] = losergrade


# stores the match in a separate CSV file
def store_match(winnerpos, loserpos, result):
    if result == 'success' or result == 'fail':
        win = 'win'
        lose = 'lose'
    elif result == 'draw':
        win = 'draw'
        lose = 'draw'
    else:
        messagebox.showerror(message='line 227 error, storing match in CSV')
    winfname = playerInfo[winnerpos][0]
    winlname = playerInfo[winnerpos][1]
    winrank = playerInfo[winnerpos][3]
    wingrade = playerInfo[winnerpos][7]

    losefname = playerInfo[loserpos][0]
    loselname = playerInfo[loserpos][1]
    loserank = playerInfo[loserpos][3]
    losegrade = playerInfo[loserpos][7]

    date = now.strftime("%Y-%m-%d")
    # store data for the winner
    playerData.append([winfname, winlname, winrank, wingrade, win,
                       losefname, loselname, loserank, losegrade, date])
    # store data for the loser
    playerData.append([losefname, loselname, loserank, losegrade, lose,
                       winfname, winlname, winrank, wingrade, date])

# if challenge is successful this function is called
# moves the loser up to the winners position
# moves everyone else in between down once
def reorder_list(winnerpos, loserpos):
    # this moves the records
    tempRecord = playerInfo[winnerpos]
    for i in range(0, (winnerpos-loserpos)):
        playerInfo[winnerpos-i] = playerInfo[winnerpos-(i+1)]
    playerInfo[loserpos] = tempRecord
    # this re-ranks the players in the right order in the main list
    playerInfoCount = 1
    for record in playerInfo:
        record[3] = playerInfoCount
        playerInfoCount +=1
    # this re-ranks the players in the right order in the ladder list
    for laddername in ladder_data_list:
        for allnames in playerInfo:
            if laddername[1] == allnames[0] + ' ' + allnames[1]:
                laddername[0] = int(allnames[3])
    ladder_data_list.sort(key=itemgetter(0))

def button_viewProfile():
    # deletes previous values
    for label in viewProfileFrame.grid_slaves():
        if int(label.grid_info()["row"]) > 1:
            label.grid_remove()
    ladder_data_list.sort(key=itemgetter(0))
    # creates the view profile buttons
    for i in range(3, len(ladder_data_list)+3):
        view_profile_button = Button(mainFrame, text='view prof',
                            command=lambda i=i: viewProfile(ladder_data_list[i-3][0]))

        view_profile_button.grid(column=int(((i-3) / 13))*6, row=((i-3) % 13)+3)

# display all the relevant info about the player
def viewProfile(rank):
    global homeImage
    raise_frame(viewProfileFrame)
    tempwins = int(playerInfo[int(rank)-1][4])
    templosses = int(playerInfo[int(rank)-1][5])
    tempdraws = int(playerInfo[int(rank)-1][6])
    # handles division by zero errors
    if tempwins + tempdraws + templosses == 0:
        winrate = 0
        lossrate = 0
    else:
        winrate = tempwins/(tempwins+tempdraws+templosses)
        lossrate = templosses/(tempwins+tempdraws+templosses)
    fifthTitle = Label(viewProfileFrame, text="Wilson's School Chess Club", font="Verdana 60 bold", pady='10')
    fifthTitle.grid(columnspan=21, row=0, sticky='W')
    homeButton5 = Button(viewProfileFrame, image=homeImage, command=lambda: raise_frame(mainFrame))
    homeButton5.grid(column=21, row=0)
    viewFnameLabel = Label(viewProfileFrame, text='First Name: ')
    viewFnameLabel.grid(row=2, column=10)
    viewFnameLabel2 = Label(viewProfileFrame, text=playerInfo[int(rank)-1][0])
    viewFnameLabel2.grid(row=2, column=11)
    viewLnameLabel = Label(viewProfileFrame, text='Last Name: ')
    viewLnameLabel.grid(row=3, column=10)
    viewLnameLabel2 = Label(viewProfileFrame, text=playerInfo[int(rank)-1][1])
    viewLnameLabel2.grid(row=3, column=11)
    viewFormLabel = Label(viewProfileFrame, text='Form: ')
    viewFormLabel.grid(row=4, column=10)
    viewFormLabel2 = Label(viewProfileFrame, text=playerInfo[int(rank)-1][2])
    viewFormLabel2.grid(row=4, column=11)
    viewRankLabel = Label(viewProfileFrame, text='Rank: ')
    viewRankLabel.grid(row=5, column=10)
    viewRankLabel2 = Label(viewProfileFrame, text=playerInfo[int(rank)-1][3])
    viewRankLabel2.grid(row=5, column=11)
    viewWinsLabel = Label(viewProfileFrame, text='Wins: ')
    viewWinsLabel.grid(row=6, column=10)
    viewWinsLabel2 = Label(viewProfileFrame, text=playerInfo[int(rank)-1][4])
    viewWinsLabel2.grid(row=6, column=11)
    viewLossesLabel = Label(viewProfileFrame, text='Losses: ')
    viewLossesLabel.grid(row=7, column=10)
    viewLossesLabel2 = Label(viewProfileFrame, text=playerInfo[int(rank)-1][5])
    viewLossesLabel2.grid(row=7, column=11)
    viewDrawsLabel = Label(viewProfileFrame, text='Draws: ')
    viewDrawsLabel.grid(row=8, column=10)
    viewDrawsLabel2 = Label(viewProfileFrame, text=playerInfo[int(rank)-1][6])
    viewDrawsLabel2.grid(row=8, column=11)
    viewGradeLabel = Label(viewProfileFrame, text='Grade: ')
    viewGradeLabel.grid(row=9, column=10)
    viewGradeLabel2 = Label(viewProfileFrame, text=playerInfo[int(rank)-1][7])
    viewGradeLabel2.grid(row=9, column=11)
    viewAttendanceLabel = Label(viewProfileFrame, text='Attendance: ')
    viewAttendanceLabel.grid(row=10, column=10)
    viewAttendanceLabel2 = Label(viewProfileFrame, text=playerInfo[int(rank)-1][8])
    viewAttendanceLabel2.grid(row=10, column=11)
    viewWinRateLabel = Label(viewProfileFrame, text='Win Rate: ')
    viewWinRateLabel.grid(row=11, column=10)
    viewWinRateLabel2 = Label(viewProfileFrame, text=(winrate))
    viewWinRateLabel2.grid(row=11, column=11)
    viewLossRateLabel = Label(viewProfileFrame, text='Loss Rate: ')
    viewLossRateLabel.grid(row=12, column=10)
    viewLossRateLabel2 = Label(viewProfileFrame, text=(lossrate))
    viewLossRateLabel2.grid(row=12, column=11)


def viewEntireLadder(start):
    global homeImage
    raise_frame(viewLadderFrame)
    fourthTitle = Label(viewLadderFrame, text="Wilson's School Chess Club", font="Verdana 60 bold", pady='10')
    fourthTitle.grid(columnspan=21, row=0, sticky='W')
    homeButton4 = Button(viewLadderFrame, image=homeImage, command=lambda: raise_frame(mainFrame))
    homeButton4.grid(column=21, row=0)
    colourcounter2 = 0
    for i in range(0, 8):
        for j in range(0, 13):
            # makes alternating colours
            if colourcounter2 == 0:
                color = '#6699ff'
                colourcounter2 = 1
            else:
                color = '#ccddff'
                colourcounter2 = 0
            # creates the table like layout
            if i % 2 == 0:
                TempLabel = Label(viewLadderFrame, height='2', bg=color)
                TempLabel.grid(column=int((i*6)/2), row=j+1, sticky='we', columnspan=1)
                if (len(playerInfo) - start) > ((int(i/2))*13)+j:
                    TempRank = Label(viewLadderFrame, text=playerInfo[start+((int(i/2)*13)+j)][3])
                    TempRank.grid(column=int((i*6)/2), row=j+1, columnspan=1)
            else:
                TempLabel = Label(viewLadderFrame, height='2', bg=color)
                TempLabel.grid(column=int((((i-1)*6)/2)+1), row=j+1, sticky='we', columnspan=5)
                if (len(playerInfo) - start) > ((int(i/2))*13)+j:
                    TempName = Label(viewLadderFrame, text=playerInfo[start+((int(i/2)*13)+j)][0] + ' ' + playerInfo[start+((int(i/2)*13)+j)][1])
                    TempName.grid(column=int((((i-1)*6)/2)+1), row=j+1, columnspan=5)

    if len(playerInfo) - start > 52:
        nextPageButton = Button(viewLadderFrame, text='Next page',
                                command=lambda: viewEntireLadder(start+52))
        nextPageButton.grid(row=15, column=0)


def addNameToArray(firstname, lastname, form):
    # makes the form uppercase and a bit of validation
    form = form.upper()
    form = form.strip()
    # makes the first letter capital
    firstname = firstname.capitalize()
    lastname = lastname.capitalize()
    # removes leading and trailing white spaces
    firstname = firstname.strip()
    lastname = lastname.strip()
    # if nothing has been entered, player can't be registered
    if firstname == '' or lastname == '' or form == '':
        messagebox.showerror(message='That is not a valid entry')
        return None
    # checks if the house is valid
    elif (form[-1:] != 'B' and form[-1:] != 'C' and form[-1] != 'D' and form[-1] != 'G' and
            form[-1:] != 'H' and form[-1:] != 'S' and form[-1:] != 'F'):
        messagebox.showerror(message='That form does not exist')
        return None
    # checks if year is valid
    elif (form[:1] != '7' and form[:1] != '8' and form[:1] != '9'
            and form[:2] != '10' and form[:2] != '11' and form[:1] != '6'):
        messagebox.showerror(message='That form does not exist')
        return None
    # checks to see if someone with same name has already been registered
    for player in playerInfo:
        if player[0] == firstname and player[1] == lastname:
            messagebox.showerror(message='There is already someone with that first name'
                                         ' and last name registered.')
            return None
    # creates a new rank; one after the last one
    newrank = int(max(int(l[3]) for l in playerInfo)) + 1
    # creates a new record and adds it to the array
    newRecord = [firstname, lastname, form, newrank, 0, 0, 0, 100, 0, now.strftime("%Y-%m-%d")]
    playerInfo.append(newRecord)

# this function will display the register screen
def registerScreen():
    global homeImage
    raise_frame(registerFrame)
    thirdTitle = Label(registerFrame, text="Wilson's School Chess Club", font="Verdana 60 bold", pady='10')
    thirdTitle.grid(columnspan=21, row=0, sticky='W')
    homeButton3 = Button(registerFrame, image=homeImage, command=lambda: raise_frame(mainFrame))
    homeButton3.grid(column=21, row=0)
    register_instructions = Label(registerFrame, font="Verdana 20",
                                 text='Type your first name, surname and your form and click'
                                      'register to be added to the ladder')
    register_instructions.grid(row=3, column=2, columnspan='20', pady='15')
    register_firstNameLabel = Label(registerFrame, text="First Name: ")
    register_firstNameLabel.grid(row=7, column=10)
    register_nameEntry = Entry(registerFrame)
    register_nameEntry.grid(row=7, column=11)
    register_surnameLabel = Label(registerFrame, text="Surname: ")
    register_surnameLabel.grid(row=8, column=10)
    register_surnameEntry = Entry(registerFrame)
    register_surnameEntry.grid(row=8, column=11)
    register_formLabel = Label(registerFrame, text="Form: ")
    register_formLabel.grid(row=9, column=10)
    register_formEntry = Entry(registerFrame)
    register_formEntry.grid(row=9, column=11)
    register_registerButton = Button(registerFrame, text='register',
                                     command=lambda: addNameToArray(register_nameEntry.get(),
                                                                     register_surnameEntry.get(),
                                                                     register_formEntry.get()))
    register_registerButton.grid(row=10, column=11)


# when sign out is clicked, this creates sign out buttons
def sign_out_buttons():
    ladder_data_list.sort(key=itemgetter(0))
    for i in range(3, len(ladder_data_list)+3):
        sign_out_button = Button(mainFrame, text='sign out',
                            command=lambda i=i: sign_out_remove(ladder_data_list[i-3][0]))

        sign_out_button.grid(column=int(((i-3) / 13))*6, row=((i-3) % 13)+3)


def sign_out_remove(rank):
    # removes the name from the list and sorts them again
    found = False
    # remove the name from the list
    for k in ladder_data_list:
        if k[0] == rank:
            ladder_data_list.remove(k)
    ladder_data_list.sort(key=itemgetter(0))
    sort_names_ladder()

# the following code is for the main page
def mainPageCode():
    # Wilson's school title and six buttons layout
    homeButton1 = Button(mainFrame, image=homeImage, command=lambda: raise_frame(mainFrame))
    homeButton1.grid(column=21, row=0)
    Sign_in = Button(mainFrame, text="Sign in", font="Verdana 15", pady='15', padx='5',
                     command=lambda: raise_frame(signInFrame))
    Sign_in.grid(column=0, row=1, columnspan=4)
    Sign_out = Button(mainFrame, text="Sign out", font="Verdana 15", pady='15', padx='5', command=sign_out_buttons)
    Sign_out.grid(column=4, row=1, columnspan=4)
    Register = Button(mainFrame, text="Register", font="Verdana 15", pady='15', padx='5', command=registerScreen)
    Register.grid(column=8, row=1, columnspan=4)
    Record = Button(mainFrame, text="Record", font="Verdana 15", pady='15', padx='5', command=window_record)
    Record.grid(column=12, row=1, columnspan=4)
    ViewLadder = Button(mainFrame, text="View Ladder", font="Verdana 15", pady='15', padx='5',
                        command=lambda: viewEntireLadder(0))
    ViewLadder.grid(column=16, row=1, columnspan=4)
    ViewProfile = Button(mainFrame, text="View Profile", font="Verdana 15", pady='15', padx='5', command=button_viewProfile)
    ViewProfile.grid(column=20, row=1, columnspan=4)

    # table for the names
    colourcounter = 0
    for i in range(0, 8):
        for j in range(0, 13):
            # makes alternating colours
            if colourcounter == 0:
                color = '#6699ff'
                colourcounter = 1
            else:
                color = '#ccddff'
                colourcounter = 0
            # creates the table like layout
            if i % 2 == 0:
                TempLabel = Label(mainFrame, height='2', bg=color)
                TempLabel.grid(column=int((i*6)/2), row=j+2, sticky='we', columnspan=1)
            else:
                TempLabel = Label(mainFrame, height='2', bg=color)
                TempLabel.grid(column=int((((i-1)*6)/2)+1), row=j+2, sticky='we', columnspan=5)
    # <--end of code for the main ladder screen-->


def signInScreenCode():
    # <--the following code is for the sign in screen-->
    # displaying and aligning labels, buttons and entries
    secondTitle = Label(signInFrame, text="Wilson's School Chess Club", font="Verdana 60 bold", pady='10')
    secondTitle.grid(columnspan=21, row=0, sticky='W')
    homeButton2 = Button(signInFrame, image=homeImage, command=lambda: raise_frame(mainFrame))
    homeButton2.grid(column=21, row=0)
    sign_in_instructions = Label(signInFrame, font="Verdana 30",
                                 text='Type either your first name or form and click search')
    sign_in_instructions.grid(row=3, column=4, columnspan='15', pady='15')
    firstNameLabel = Label(signInFrame, text="First Name: ")
    firstNameLabel.grid(row=7, column=10)
    nameEntry = Entry(signInFrame)
    nameEntry.grid(row=7, column=11)
    nameEntryButton = Button(signInFrame, text='Search name', command=lambda: search_player(nameEntry.get(), 'name'))
    nameEntryButton.grid(row=7, column=12)
    formLabel = Label(signInFrame, text="Form: ")
    formLabel.grid(row=8, column=10)
    formEntry = Entry(signInFrame)
    formEntry.grid(row=8, column=11)
    formEntryButton = Button(signInFrame, text='Search form', command=lambda: search_player(formEntry.get(), 'form'))
    formEntryButton.grid(row=8, column=12)
    # <--end of code for sign in screen-->


# depending on whether a name or form is enter, this will search through csv file
def search_player(value, whatType):
    found = False
    counter = 0
    global sign_in_data_list
    sign_in_data_list = []
    # removes the pre-existing search items
    for label in signInFrame.grid_slaves():
        if int(label.grid_info()["row"]) > 11:
            label.grid_remove()
    if str(whatType) == 'form':
        value = value.upper()
        for form in range(0, len(playerInfo)):
            if str(playerInfo[form][2]) == value:
                # if the form is found, passes it onto a function to add to the grid
                show_search_player(playerInfo[form][3], playerInfo[form][0],
                                   playerInfo[form][1], 12+counter)
                counter += 1
                found = True
        # if the form is not found, an error message will pop up
        if not found:
            messagebox.showerror('Error', 'That form does not exist')
    elif str(whatType) == 'name':
        # turns search value into correct format
        value = value.lower()
        value = value.title()
        for name in range(0, len(playerInfo)):
            if str(playerInfo[name][0]) == value:
                show_search_player(playerInfo[name][3], playerInfo[name][0],
                                   playerInfo[name][1], 12+counter)
                counter += 1
                found = True
        if not found:
            messagebox.showerror('Error', 'That name does not exist')


# displays the relevant names and forms in a grid below
def show_search_player(rank, fname, lname, row):
    global sign_in_data_list
    ranklabel = Label(signInFrame, text=rank)
    ranklabel.grid(row=row, column=9)
    fnamelabel = Label(signInFrame, text=fname)
    fnamelabel.grid(row=row, column=10)
    lnamelabel = Label(signInFrame, text=lname)
    lnamelabel.grid(row=row, column=11)
    addButtonlabel = Button(signInFrame, text='select', command=lambda: add_name(row))
    addButtonlabel.grid(row=row, column=12)
    # adds the row, rank, fname and lname into a temporary list
    sign_in_data_list.append([row, rank, fname, lname])


# when button is pressed searches through the temporary list for matching data
def add_name(row):
    global sign_in_data_list
    for sublist in sign_in_data_list:
        if sublist[0] == row:
            combinedname = sublist[2] + ' ' + sublist[3]
            # once it's found, the rank and name are passed down to check if they are
            # already on the ladder
            check_name(sublist[1], combinedname)


# checks if that name is already on the ladder
def check_name(rank, name):
    ladder_exists = False
    # this 'if' checks if there's any space in the main ladder
    if len(ladder_data_list) >= 52:
        messagebox.showerror('error', 'Maximum number of people signed in')
        return None
    for i in ladder_data_list:
        if int(i[0]) == int(rank):
            ladder_exists = True
            # if it's already there, an error message pops up
            messagebox.showerror('error', 'that name is already on the ladder')
    if not ladder_exists:
        # if not, then the data is added to the main ladder screen list
        ladder_data_list.append([int(rank), name])
        # function to sort the names into the right order
        sort_names_ladder()
        # finds the name in list and indicates they've signed in
        for ranksearch in playerInfo:
            if int(ranksearch[3]) == int(rank):
                ranksearch[8] = 0
                ranksearch[9] = now.strftime("%Y-%m-%d")
                break


# function to sort the names into the right order
def sort_names_ladder():
    global ladderCounter
    ladderCounter = 3
    ladder_data_list.sort(key=itemgetter(0))
    # add all the names to the ladder
    clear_names_ladder()
    for i in range(0, len(ladder_data_list)):
        addranklabel = Label(mainFrame, text=ladder_data_list[i][0])
        addnamelabel = Label(mainFrame, text=ladder_data_list[i][1])

        addranklabel.grid(row=((i)%13)+3, column=int((i/13))*6, columnspan=1)
        addnamelabel.grid(row=((i)%13)+3, column=(int(i/13)*6)+1, columnspan=5)
        # ladderCounter += 1

def clear_names_ladder():
    # removes all the previous labels on the grid
    for label in mainFrame.grid_slaves():
        if int(label.grid_info()["row"]) > 2:
            label.grid_remove()
    # adds the empty coloured labels on to the grid
    colourcounter = 0
    for i in range(0, 8):
        for j in range(0, 13):
            # makes alternating colours
            if colourcounter == 1:
                color = '#6699ff'
                colourcounter = 0
            else:
                color = '#ccddff'
                colourcounter = 1
            # creates the table like layout
            if i % 2 == 0:
                TempLabel = Label(mainFrame, height='2', bg=color)
                TempLabel.grid(column=int((i*6)/2), row=j+3, sticky='we', columnspan=1)
            else:
                TempLabel = Label(mainFrame, height='2', bg=color)
                TempLabel.grid(column=int((((i-1)*6)/2)+1), row=j+3, sticky='we', columnspan=5)


# fix resizing issue
def resize():
    for r in frame_names:
        for x in range(50):
            Grid.columnconfigure(r, x, weight=1)
        for y in range(50):
            Grid.columnconfigure(r, y, weight=1)

# before closing, it will confirm and save data to the csv file
def on_closing():
    if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
        # converting lists to csv for playerinfo
        with open("playerinfo.csv", 'wt', newline='') as h:
            ListToCsv = csv.writer(h)
            ListToCsv.writerows(playerInfo)
        # converting lists to csv for playerdata
        with open("matchhistory.csv", 'wt', newline='') as k:
            ListToCsv2 = csv.writer(k)
            ListToCsv2.writerows(playerData)
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
raise_frame(mainFrame)
resize()
mainPageCode()
signInScreenCode()
check_attendance()
root.mainloop()

