#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, requests, random, re
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.views import generic

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

PAGE_ACCESS_TOKEN ='EAALmSKOyvQQBAJDMaeRoLz8An75ZC9LhMrMqO8t7nzkf97H1YzdnVrvFwSvPSZBdUch1RIVb51nM5P2q8GvNPYZCQATam8V4qIuAZBolhN0pHczH4143zFBts546O8ZBj05exL3j58lvHlTcSom2SL7vnyJi7vKgUALZBgHCluxgZDZD'
VERIFY_TOKEN = '9582648830'

quotes_arr = [["Life isn’t about getting and having, it’s about giving and being.", "Kevin Kruse"],
["Whatever the mind of man can conceive and believe, it can achieve.", "Napoleon Hill"],
["Strive not to be a success, but rather to be of value.", "Albert Einstein"],
["Two roads diverged in a wood, and I—I took the one less traveled by, And that has made all the difference.", "Robert Frost"],
["I attribute my success to this: I never gave or took any excuse.", "Florence Nightingale"],
["You miss 100% of the shots you don’t take.", "Wayne Gretzky"],
["I’ve missed more than 9000 shots in my career. I’ve lost almost 300 games. 26 times I’ve been trusted to take the game winning shot and missed. I’ve failed over and over and over again in my life. And that is why I succeed.", "Michael Jordan"],
["The most difficult thing is the decision to act, the rest is merely tenacity.", "Amelia Earhart"],
["Every strike brings me closer to the next home run.", "Babe Ruth"],
["Definiteness of purpose is the starting point of all achievement.", "W. Clement Stone"],
["We must balance conspicuous consumption with conscious capitalism.", "Kevin Kruse"],
["Life is what happens to you while you’re busy making other plans.", "John Lennon"],
["We become what we think about.", "Earl Nightingale"],
["14.Twenty years from now you will be more disappointed by the things that you didn’t do than by the ones you did do, so throw off the bowlines, sail away from safe harbor, catch the trade winds in your sails.  Explore, Dream, Discover.", "Mark Twain"],
["15.Life is 10% what happens to me and 90% of how I react to it.", "Charles Swindoll"],
["The most common way people give up their power is by thinking they don’t have any.", "Alice Walker"],
["The mind is everything. What you think you become.", "Buddha"],
["The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"],
["An unexamined life is not worth living.", "Socrates"],
["Eighty percent of success is showing up.", "Woody Allen"],
["Your time is limited, so don’t waste it living someone else’s life.", "Steve Jobs"],
["Winning isn’t everything, but wanting to win is.", "Vince Lombardi"],
["I am not a product of my circumstances. I am a product of my decisions.", "Stephen Covey"],
["Every child is an artist.  The problem is how to remain an artist once he grows up.", "Pablo Picasso"],
["You can never cross the ocean until you have the courage to lose sight of the shore.", "Christopher Columbus"],
["I’ve learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel.", "Maya Angelou"],
["Either you run the day, or the day runs you.", "Jim Rohn"],
["Whether you think you can or you think you can’t, you’re right.", "Henry Ford"],
["The two most important days in your life are the day you are born and the day you find out why.", "Mark Twain"],
["Whatever you can do, or dream you can, begin it.  Boldness has genius, power and magic in it.", "Johann Wolfgang von Goethe"]]

def return_random_quote():
    random.shuffle(quotes_arr)
    return quotes_arr[0]

def post_facebook_message(fbid, recevied_message):
    reply_text = recevied_message + ':-)' + return_random_quote()

    try:
        user_details_url = "https://graph.facebook.com/v2.6/%s" % fbid
        user_details_params = {'fields': 'first_name,last_name,profile_pic', 'access_token': PAGE_ACCESS_TOKEN}
        user_details = requests.get(user_details_url, user_details_params).json()
        joke_text = 'Yo ' + user_details['first_name'] + '..! ' + reply_text
    except:
        joke_text = 'Yo ' + reply_text

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())


class MyQuoteBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
                    post_facebook_message(message['sender']['id'], message['message']['text'])

        return HttpResponse()


def index(request):
    print test()
    print return_random_quote()
    return HttpResponse("Hello World")


def test():
    post_facebook_message('sachin.gupta.18400', 'bot working')