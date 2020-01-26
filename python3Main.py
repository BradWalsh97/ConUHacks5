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
            text=f"Starting work session!",
            thread_ts=thread_ts
        )
        directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp_capture")
        image_capture.start_capturing(20, 5, directory)
        web_client.chat_postMessage(
            channel=channel_id,
            text=f"work session done. Enter \"Break\" to start your break",
            thread_ts=thread_ts
        )

    elif 'Break' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Starting break!",
            thread_ts=thread_ts
        )
        time.sleep(5 * 60)
        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Break done!",
            thread_ts=thread_ts
        )

    elif 'calibrate right' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']
        image_capture.capture_image(image_capture.calibration_directory, "calibrate-right.png")

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Calibrated right side of monitor",
            thread_ts=thread_ts
        )

    elif 'calibrate left' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']
        image_capture.capture_image(image_capture.calibration_directory, "calibrate-left.png")

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Calibrated left side of monitor",
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

slack_token = "xoxb-924236022790-922171684224-BAM1JLfF35k3CLWhReFUKkwN"
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()


