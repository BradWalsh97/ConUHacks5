import os
import slack
import image_capture
import time



@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']

    if 'Hello' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        #user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Hi <@{user}>!",
            thread_ts=thread_ts
        )
    elif 'pomodoro start' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        #user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Starting work session!",
            thread_ts=thread_ts
        )
        directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pomodoro")
        image_capture.start_capturing(20, 5, directory)
        web_client.chat_postMessage(
            channel=channel_id,
            text=f"work session done. Enter \"Break\" to start your break",
            thread_ts=thread_ts
        )

    elif 'break' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        #user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Starting break!",
            thread_ts=thread_ts
        )
        time.sleep(5 * 60)
        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Break done! enter \"Start\" to start another pomodoro",
            thread_ts=thread_ts
        )

    elif 'calibrate' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        #user = data['user']

        direction = data.get('text', []).split(' ')[1]

        image_capture.capture_image(image_capture.calibration_directory, "calibrate-" + direction + ".png")

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Calibrated "+ direction + " side of monitor",
            thread_ts=thread_ts
        )


#slack_token = os.environ["SLACK_BOT_TOKEN"]
directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp_capture")
if not os.path.isdir(directory):
    os.mkdir(directory)

if not os.path.isdir(image_capture.pomodoro_directory):
    os.mkdir(image_capture.pomodoro_directory)
if not os.path.isdir(image_capture.calibration_directory):
    os.mkdir(image_capture.calibration_directory)

slack_token = "xoxb-924236022790-922171684224-Zm5zWG9uPWxXnX2pA2cAydmU"
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()



