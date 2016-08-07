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


def post_facebook_message(fbid, recevied_message):
    reply_text = recevied_message + ':)'

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
    return HttpResponse("Hello World")


def test():
    post_facebook_message('sachin.gupta.18400', 'bot working')