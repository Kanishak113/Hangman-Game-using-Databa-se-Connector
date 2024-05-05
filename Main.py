import mysql.connector
import random
import time
mydb = mysql.connector.connect(
        user='root',
        password='',
        database='Leaderboard'
    )
print("\nWelcome to Hangman game\n")
name = input("Enter your name: ")
print("Hello " + name + "! Best of Luck!")
time.sleep(2)
print("The game is about to start!\n Let's play Hangman!")
time.sleep(3)
def main():
    global count
    global display
    global word
    global currentword
    global already_guessed
    global length
    global play_game
    words_to_guess = ["january","border","image","film","promise","kids","lungs","doll","rhyme","damage"
                   ,"plants"]
    word = random.choice(words_to_guess)
    currentword=word
    length = len(word)
    count = 0
    display = '_' * length
    already_guessed = []
    play_game = ""
    print("You will get a score out of",length)
def play_loop():
    global play_game
    play_game = input("Do You want to play again? y = yes, n = no \n")
    while play_game not in ["y", "n","Y","N"]:
        play_game = input("Do You want to play again? y = yes, n = no \n")
    if play_game == "y":
        main()
    elif play_game == "n":
        print("Thanks For Playing! We expect you back again!")
        exit()
def hangman():
    global count
    global display
    global word
    global already_guessed
    global outof
    global play_game
    outof=len(already_guessed)
    limit = 5
    guess = input("This is the Hangman Word: " + display + " Enter your guess: \n")
    guess = guess.strip()
    if len(guess.strip()) == 0 or len(guess.strip()) >= 2 or guess <= "9":
        print("Invalid Input, Try a letter\n")
        hangman()
    elif guess in word:
        already_guessed.extend([guess])
        index = word.find(guess)
        word = word[:index] + "_" + word[index + 1:]
        display = display[:index] + guess + display[index + 1:]
        print(display + "\n")
    elif guess in already_guessed:
        print("Try another letter.\n")
    else:
        count += 1
        if count == 1:
            time.sleep(1)
            print("   _____ \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "__|__\n")
            print("Wrong guess. " + str(limit - count) + " guesses remaining\n")
        elif count == 2:
            time.sleep(1)
            print("   _____ \n"
                  "  |     | \n"
                  "  |     |\n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "__|__\n")
            print("Wrong guess. " + str(limit - count) + " guesses remaining\n")
        elif count == 3:
           time.sleep(1)
           print("   _____ \n"
                 "  |     | \n"
                 "  |     |\n"
                 "  |     | \n"
                 "  |      \n"
                 "  |      \n"
                 "  |      \n"
                 "__|__\n")
           print("Wrong guess. " + str(limit - count) + " guesses remaining\n")
        elif count == 4:
            time.sleep(1)
            print("   _____ \n"
                  "  |     | \n"
                  "  |     |\n"
                  "  |     | \n"
                  "  |     O \n"
                  "  |      \n"
                  "  |      \n"
                  "__|__\n")
            print("Wrong guess. " + str(limit - count) + " last guess remaining\n")
        elif count == 5:
            time.sleep(1)
            print("   _____ \n"
                  "  |     | \n"
                  "  |     |\n"
                  "  |     | \n"
                  "  |     O \n"
                  "  |    /|\ \n"
                  "  |    / \ \n"
                  "__|__\n")
            print("Wrong guess. You loss and were hanged!!!\n")
            time.sleep(2)
            print("The alphabets you gussed:",already_guessed)
            time.sleep(2)
            print("The word was",currentword)
            time.sleep(2)
            print("Your Score is = ",outof,"/",length)
            percent=int((outof/length)*100)
            time.sleep(2)
            mycursor = mydb.cursor()
            sql = "INSERT INTO Scores(Name,Score,Out_of,percentage) VALUES(%s,%s,%s,%s)"
            val = (name,outof,length,percent)
            mycursor.execute(sql, val)
            print("Your Score has been registered\n")
            mydb.commit()
            dbcursor=mydb.cursor()
            dbcursor.execute("SELECT * FROM Scores ORDER BY percentage DESC")
            time.sleep(2)
            print("The current Scoreboard is:")
            time.sleep(2)
            print("[Name,Score,Out of,Percentage]")
            for data in dbcursor:
                time.sleep(1)
                print("[",data,"]")
            play_loop()
    if word == '_' * length:
        time.sleep(2)
        print("Congrats! You have guessed the word correctly!")
        time.sleep(2)
        print("Your Score is= ",length,"/",length)
        percent = int((length / length) * 100)
        outof=length
        time.sleep(2)
        mycursor = mydb.cursor()
        sql = "INSERT INTO Scores(Name,Score,Out_of,percentage) VALUES(%s,%s,%s,%s)"
        val = (name,outof,length,percent)
        mycursor.execute(sql, val)
        print("Your Score has been registered\n")
        time.sleep(3)
        mydb.commit()
        dbcursor = mydb.cursor()
        dbcursor.execute("SELECT * FROM Scores ORDER BY percentage DESC")
        print("The current Scoreboard is:")
        time.sleep(2)
        print("[Name,Score,Out of,Percentage]")
        for data in dbcursor:
            time.sleep(1)
            print("[",data,"]")
        play_loop()
    elif count != limit:
        hangman()
main()
hangman()
