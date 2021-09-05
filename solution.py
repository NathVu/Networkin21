
def welcome_assignment_answers(question):
    if question == "Are encoding and encryption the same? - Yes/No":
        answer = "No"
    elif question == "Is it possible to decrypt a message without a key? - Yes/No":
        answer = "Yes"
    elif question == "In Slack, what is the secret passphrase posted in the " \
                     "#cyberfellows-computernetworking-fall2021 channel posted by a TA?":
        answer = "mTLS"
    elif question == "Is it possible to decode a message without a key?":
        answer = "Yes"
    elif question == "Is a hashed message supposed to be un-hashed?":
        answer = "No"
    elif question == "What is the MD5 hashing value to the following message: 'NYU Computer Networking'":
        answer = "42b76fe51778764973077a5a94056724"
    elif question == "Is MD5 a secured hashing algorithm?":
        answer = "Yes"
    elif question == "What layer from the TCP/IP model the protocol DHCP belongs to?":
        answer = 3
    elif question == "What layer of the TCP/IP model the protocol TCP belongs to?":
        answer = 2
    return(answer)
# Complete all the questions.



if __name__ == "__main__":
    #use this space to debug and verify that the program works
    debug_question = "Are encoding and encryption the same? - Yes/No"
    print(welcome_assignment_answers(debug_question))
