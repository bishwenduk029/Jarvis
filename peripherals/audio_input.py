import sys

from playsound import playsound
from speech_recognition import (Microphone, Recognizer, RequestError,
                                UnknownValueError, WaitTimeoutError)

recognizer = Recognizer()


def listener(timeout: int, phrase_limit: int, sound: bool = True) -> str:
    """Function to activate listener, this function will be called by most upcoming functions to listen to user input.

    Args:
        timeout: Time in seconds for the overall listener to be active.
        phrase_limit: Time in seconds for the listener to actively listen to a sound.
        sound: Flag whether or not to play the listener indicator sound. Defaults to True unless set to False.

    Returns:
        str:
         - On success, returns recognized statement from the microphone.
         - On failure, returns ``SR_ERROR`` as a string which is conditioned to respond appropriately.
    """
    try:
        with Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            sys.stdout.write("\rListener activated..") and playsound('../indicators/start.mp3') if sound else \
                sys.stdout.write("\rListener activated..")
            listened = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
            sys.stdout.write("\r") and playsound('../indicators/end.mp3') if sound else sys.stdout.write("\r")
            return_val = recognizer.recognize_google(listened)
            sys.stdout.write(f'\r{return_val}')
    except (UnknownValueError, RequestError, WaitTimeoutError):
        return_val = 'SR_ERROR'
    return return_val
