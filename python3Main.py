import os
import shutil
import slack
import image_capture
from azureFaceAPI_Basic import pomodoro_session_analysis
import time

session_length = 5 * 50
session_stats = []

# from stack overflow
def delete_contents(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']

    if 'pomodoro start' in data.get('text', []):
        channel_id = data['channel']

        delete_contents(image_capture.pomodoro_directory)

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Starting work session!"
        )
        directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pomodoro")
        image_capture.start_capturing(20, 5, directory)
        web_client.chat_postMessage(
            channel=channel_id,
            text=f"work session done. Enter \"Break\" to start your break"
        )    

    elif 'break' in data.get('text', []):
        channel_id = data['channel']

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Starting break!"
        )
        time.sleep(5 * 60)
        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Break done! enter \"Start\" to start another pomodoro"
        )

    elif 'calibrate' in data.get('text', []):
        channel_id = data['channel']

        direction = data.get('text', []).split(' ')[1]
        image_capture.capture_image(image_capture.calibration_directory, "calibrate-" + direction + ".png")

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Calibrated "+ direction + " side of monitor"
        )

    elif 'set session length' in data.get('text', []):
        channel_id = data['channel']
        session_length = data.get('text', []).split()[3] * 60
        web_client.chat_postMessage(
            channel=channel_id,
            text=f"changed session length to " + str(session_length),
        )

    elif 'test' in data.get('text', []):
        channel_id = data['channel']

        delete_contents(image_capture.pomodoro_directory)
        image_capture.capture_image(image_capture.pomodoro_directory, "capture0.png")
        result = pomodoro_session_analysis()
        web_client.chat_postMessage(
            channel=channel_id,
            text=f"result: " + str(result),
        )

#slack_token = os.environ["SLACK_BOT_TOKEN"]
directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp_capture")
if not os.path.isdir(directory):
    os.mkdir(directory)

if not os.path.isdir(image_capture.pomodoro_directory):
    os.mkdir(image_capture.pomodoro_directory)
if not os.path.isdir(image_capture.calibration_directory):
    os.mkdir(image_capture.calibration_directory)

slack_token = "xoxb-924236022790-922171684224-wRB04EUeIOZPUKzOFqeRCt4k"
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()
if __name__ == "__main__":
    directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp_capture")
    if not os.path.isdir(directory):
        os.mkdir(directory)

    if not os.path.isdir(image_capture.pomodoro_directory):
        os.mkdir(image_capture.pomodoro_directory)
    if not os.path.isdir(image_capture.calibration_directory):
        os.mkdir(image_capture.calibration_directory)




