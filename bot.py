#!/usr/bin/python3

from irc import *
import os, random, time, threading, signal

# list of quotes available to send
QUOTES = [
'Make friends first, make sales second, make love third. In no particular order.',
'Well, it\'s love at first sight. Actually, it was... No, it was when I heard her voice. It was love at first see with my ears.',
'No, I\'m not going to tell them about the downsizing. If a patient has cancer, you don\'t tell them.',
'An office is for not dying. An office is a place to live life to the fullest, to the max, to... An office is a place where dreams come true.',
'Wikipedia is the best thing ever. Anyone in the world can write anything they want about any subject. So you know you are getting the best possible information.',
'Guess what, I have flaws. What are they? Oh I don\'t know. I sing in the shower. Sometimes I spend too much time volunteering. Occasionally I\'ll hit somebody with my car. So sue me.',
'Do I need to be liked? Absolutely not. I like to be liked. I enjoy being liked. I have to be liked, but it\'s not like this compulsive need to be liked, like my need to be praised.',
'I love inside jokes. I\'d love to be a part of one someday.',
'I guess I’ve been working so hard, I forgot what it’s like to be hardly working.',
'I don\'t hate it. I just don\'t like it at all and it\'s terrible.',
'I\'m not superstitious but I am a little stitious.',
'I am Beyonce, always.',
'Fool me once, strike one. Fool me twice, strike three.',
'I would say I kind of have an unfair advantage, because I watch reality dating shows like a hawk, and I learn. \
I absorb information from the strategies of the winners and the losers. Actually, I probably learn more from the losers.',
'Don\'t ever, for any reason, do anything for anyone, for any reason, ever, no matter what. No matter where. Or who, or \
who you are with, or where you are going or... or where you\'ve been... ever. For any reason, whatsoever.',
'Abraham Lincoln once said that, \'If you\'re a racist, I will attack you with the North.\' \
And those are the principles that I carry with me in the workplace.',
'I don\'t understand. We have a day honoring Martin Luther King, but he didn\'t even work here.',
'I feel like all my kids grew up and then they married each other. It\'s every parents\' dream.',
'Here it is, heart of New York City, Times Square... named for the good times you have when you\'re in it.',
'Two weeks ago, I was in the worst relationship of my life. She treated me poorly, we didn\'t connect, I was miserable. \
Now, I am in the best relationship of my life, with the same woman. Love is a mystery.',
'Hi, I\'m Date Mike. Nice to meet me. How do you like your eggs in the morning?',
'I took her to the hospital. And the doctors tried to save her life, they did the best they could. And she is going to be okay.',
'This is our receptionist, Pam. If you think she\'s cute now you should have seen her a couple years ago.',
'Presents are the best way to show someone how much you care. It\'s like this tangible thing that you can point to and \
say, \'Hey, man, I love you this many dollars worth.\''
'I would not miss it for the world. But if something else came up I would definitely not go.',
'If I had a gun with two bullets and I was in a room with Hitler, Bin Laden and Toby, I would shoot Toby twice.',
'I don\'t come up with this stuff, I just forward it along. You wouldn\'t arrest the guy who was \
just passing drugs from one guy to another.',
'I had a great summer. I got west nile virus, lost a ton of weight. Then I went back to the lake. And I \
stepped on a piece of glass in the parking lot, which hurt. That got infected. Even though I peed on it...',
'Yes it is true! I, Michael Scott, am signing up with an online dating service. I need a username and \
I have a great one. Little Kid Lover. That way people will know exactly where my priorities are at.',
'If you break that girl\'s heart, I will kill you. That\'s just a figure of speech. \
But seriously, if you break that girl\'s heart, I will literally kill you and your entire family.',
'I think Angela might be gay. Could Oscar and Angela be having a gay affair? Maybe! Is that what this is about?',
'That was offensive and lame. So double offensive. This is an environment of welcoming and you should just get the hell out of here.',
'Oh, this is gonna feel so good getting this thing off my chest... that\'s what she said.',
'You may look around and see two groups here: white collar, blue collar. \
But I don\'t see it that way, and you know why not? Because I am collar-blind.',
'You cheated on me? When I specifically asked you not to?',
'I am running away from my responsibilities. And it feels good.',
'do you think doing alcohol is cool?',
'I\'m prison Mike!',
'You know why they call me prison Mike?!',
'hey, hey, hey, hey, that\'s just the way we talk in the clink.',
'I AM HERE TO SCARE YOU STRAIIIGHT!!',
'Oh, and you. You, my friend, would be da belle of da ball in prison.\
Don\'t drop the soap! Don\'t drop the soap!',
'Look, prison stinks, is what I\'m saying. It\'s not like you can go home, and, \
recharge your batteries, and come back in the morning and, be with your friends\
, having fun in the office.',
'I stole. ... And I robbed. And I kidnapped... the... president\'s son. And \
held him for ransom. And I nevah got caught, neither.',
'Gruel. Sandwiches. Gruel omelettes. Nothing but gruel. Plus, you can eat your \
own hair.',
'The worst thing about prison was the... was the Dementors. They... were flying \
all over the place, and they were scary. And they\'d come down, and they\'d suck \
the soul out of your body, and it hurt!',
'This place is freaking awesome! The people are awesome! Your boss is nice! \
Everyone seems to get along! People are tolerant! People who... have jumped to \
conclusions can redeem themselves!'
'I hope that this scared you. And from me, Prison Mike, to you, I just wanna \
thank you for listening to me. Letting me be a part of your life today.',
'If you think is prison is so wonderful, then, enjoy prison! They are such \
babies. I am going to leave them in there until they can appreciate what it\'s \
like to have freedom. And if this doesn\'t bother them, then I am out of ideas.'
]

def send_quote(irc, channel, lower_range, upper_range):
    random_int = random.randint(lower_range, upper_range)
    time.sleep(random_int)

    irc.send(channel, random.choice(QUOTES))


def main():
    try:
        # IRC server IP address
        server = "127.0.0.1"

        # IRC server port number
        port = 6667

        # Channel to post to
        channel = "#quotes"

        # Bot nick name (won't show up in mIRC)
        botnick = "michael_scott"
        # Bot username if necessary
        botnickpass = "prison_mike"
        # Bot password if necessary
        botpass = "<%= @dunder_mifflin_rocks %>"
        # lower range of random message sending in seconds
        lower_range = 1
        # upper range of random message sending in seconds
        upper_range = 15

        irc = IRC()
        irc.connect(server, port, channel, botnick, botpass, botnickpass)

        ping_catcher = threading.Thread(target=irc.get_text).start()

        text = irc.get_text()

        while 1:
#           print(text)        ## UNCOMMENT FOR DEBUGGING
            # sends random quote from QUOTES list to server and channel

           send_quote(irc, channel, lower_range, upper_range)

    except KeyboardInterrupt:
        irc.send(channel, "/QUIT \r\n")
        print("Disconnected from server.")


if __name__ == '__main__':
    main()

