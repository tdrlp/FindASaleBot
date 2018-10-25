import praw
import smtplib
import config
import os

# subreddit to browse
SUB = "bapcsalescanada"

# terms to search for, must match all terms inside the arrays
searchCriterias = [["1080", "GTX"],["1070", "GTX"]]

def main():
    reddit = praw.Reddit("yute")
    subreddit = reddit.subreddit(SUB)

    if not os.path.isfile("sent_emails.txt"):
        sentEmails = []
    else:
        with open("sent_emails.txt", "r") as file:
            sentEmails = file.read()
            sentEmails = sentEmails.split("\n")

            # filter out the blank values
            sentEmails = list(filter(None, sentEmails))

    # check the 50 newest posts
    for submission in subreddit.new(limit=5):
        titleText = submission.title.split(" ")

        # loop through all the lists containing matching criteria
        for lst in searchCriterias:
            matchingWordsCounter = 0

            # loop through each criterion in the lists
            for criterion in lst:
                # loop through all the words in the title
                for word in titleText:
                    if word == criterion:
                        matchingWordsCounter += 1

            # check if a matching post was found
            if matchingWordsCounter == len(lst):
                print("A match was found! Sending a notification ...")
                if submission.id not in sentEmails:
                    sendEmail(submission.title, "The bot has found an item!\n\n" +
                    submission.title + "\n\nCheck reddit now!")

                    # add that an email about this submission was sent
                    sentEmails.append(submission.id)

    # update the file
    with open("sent_emails.txt", "w") as file:
        for id in sentEmails:
            file.write(id + "\n")

def sendEmail(title, content):
    with smtplib.SMTP("smtp.gmail.com:587") as mail:
        mail.ehlo()
        mail.starttls()
        mail.login(config.EMAIL, config.PASSWORD)
        message = "Subject: {}\n\n{}".format(title, content)
        mail.sendmail(config.EMAIL, config.EMAIL, message)
        mail.quit()
        print("\t>> Success: Notification sent!")

if __name__ == "__main__":
    main()
