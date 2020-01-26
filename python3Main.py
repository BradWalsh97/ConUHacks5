import os
import slack

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if 'Hello' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Hi <@{user}>!",
            thread_ts=thread_ts
        )
    elif 'Pomodoro Start' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Startin' that shit for ya <@{user}>!",
            thread_ts=thread_ts
        )

#slack_token = os.environ["SLACK_BOT_TOKEN"]
#slack_token = "xoxb-924236022790-922171684224-boLaUwt35ZtvN8plCj6e12kj"
slack_token = "xoxb-924236022790-922171684224-S1VbuJXNAb8mlvkph90LxJqE"
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()
