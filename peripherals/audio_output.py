import sys
from os import environ
from random import choice

import pyttsx3

from components.acknowledgement_words import ack
from helper_functions.keywords import Keywords
from helper_functions.logger import logger
from peripherals.audio_input import listener

speaker = pyttsx3.init()
keywords = Keywords()


# noinspection PyUnresolvedReferences,PyProtectedMember
def say(text: str = None, run: bool = False) -> None:
    """Calls speaker.say to speak a statement from the received text.

    Args:
        text: Takes the text that has to be spoken as an argument.
        run: Takes a boolean flag to choose whether or not to run the speaker.say loop.
    """
    if text:
        speaker.say(text=text)
        text = text.replace('\n', '\t').strip()
        logger.info(f'Response: {text}')
        logger.info(f'Speaker called by: {sys._getframe(1).f_code.co_name}')
        sys.stdout.write(f"\r{text}")
        environ['text_spoken'] = text
    if run:
        speaker.runAndWait()


# noinspection PyUnresolvedReferences,PyTypeChecker
def voice_default(voice_model: str = 'Daniel') -> None:
    """Sets voice module to default.

    Args:
        voice_model: Defaults to ``Daniel`` in mac.
    """
    voices = speaker.getProperty("voices")  # gets the list of voices available
    for ind_d, voice_d in enumerate(voices):
        if voice_d.name == voice_model:
            sys.stdout.write(f'\rVoice module has been re-configured to {ind_d}::{voice_d.name}')
            speaker.setProperty("voice", voices[ind_d].id)
            return


# noinspection PyUnresolvedReferences,PyTypeChecker
def voice_changer(phrase: str = None) -> None:
    """Speaks to the user with available voices and prompts the user to choose one.

    Args:
        phrase: Initiates changing voices with the model name. If none, defaults to ``Daniel``
    """
    if not phrase:
        voice_default()
        return

    voices = speaker.getProperty("voices")  # gets the list of voices available
    choices_to_say = ['My voice module has been reconfigured. Would you like me to retain this?',
                      "Here's an example of one of my other voices. Would you like me to use this one?",
                      'How about this one?']

    for ind, voice in enumerate(voices):
        speaker.setProperty("voice", voices[ind].id)
        say(text=f'I am {voice.name} sir!')
        sys.stdout.write(f'\rVoice module has been re-configured to {ind}::{voice.name}')
        say(text=choices_to_say[ind]) if ind < len(choices_to_say) else say(text=choice(choices_to_say))
        say(run=True)
        keyword = listener(timeout=3, phrase_limit=3)
        if keyword == 'SR_ERROR':
            voice_default()
            say(text="Sorry sir! I had trouble understanding. I'm back to my default voice.")
            return
        elif 'exit' in keyword or 'quit' in keyword or 'Xzibit' in keyword:
            voice_default()
            say(text='Reverting the changes to default voice module sir!')
            return
        elif any(word in keyword.lower() for word in keywords.ok):
            say(text=choice(ack))
            return
