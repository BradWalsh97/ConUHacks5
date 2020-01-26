import os
import shutil
import slack
import image_capture
from azureFaceAPI_Basic import pomodoro_session_analysis
import time

session_length = 1 * 60
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

    global session_length
    global session_stats

    if 'start' == data.get('text', []):
        channel_id = data['channel']

        delete_contents(image_capture.pomodoro_directory)

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Beginning work session for %d minutes!" % (session_length / 60)
        )

        directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pomodoro")
        image_capture.start_capturing(session_length, 5, directory)
        web_client.chat_postMessage(
            channel=channel_id,
            text=f"work session done!"
        )
        result = pomodoro_session_analysis()  
        print("result: " + str(result))
        session_stats.append(result)

    elif 'break' in data.get('text', []):
        channel_id = data['channel']

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Starting rest period!"
        )
        time.sleep(5)
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
        session_length = int(data.get('text', []).split()[3]) * 60
        web_client.chat_postMessage(
            channel=channel_id,
            text=f"changed session length to " + str(session_length/60),
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

    elif 'get stats' in data.get('text', []):
        channel_id = data['channel']
        text = "stat history:\n"
        for i, stat in enumerate(session_stats):
            text += f"session %d: %.1f%% focused\n" % ((i + 1), stat * 100)
        web_client.chat_postMessage(
            channel=channel_id,
            text=text,
        )

        if session_stats[-1] < 1.0:
            web_client.chat_postMessage(
            channel=channel_id,
            text=f"Based on your last session I recommend you decrease you work session by %.1f minutes" % ((session_length * (1 - session_stats[-1])) / 60)
        )

#slack_token = os.environ["SLACK_BOT_TOKEN"]
directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp_capture")
if not os.path.isdir(directory):
    os.mkdir(directory)

if not os.path.isdir(image_capture.pomodoro_directory):
    os.mkdir(image_capture.pomodoro_directory)
if not os.path.isdir(image_capture.calibration_directory):
    os.mkdir(image_capture.calibration_directory)

slack_token = "xoxb-924236022790-922171684224-NXgEH5e6jN2QxEGVMilnhsBM"
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()
if __name__ == "__main__":

    if not os.path.isdir(image_capture.pomodoro_directory):
        os.mkdir(image_capture.pomodoro_directory)
    if not os.path.isdir(image_capture.calibration_directory):
        os.mkdir(image_capture.calibration_directory)