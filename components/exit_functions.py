from datetime import datetime

from components.events import celebrate

weekend = ['Friday', 'Saturday']


def exit_message() -> str:
    """Variety of exit messages based on day of week and time of day.

    Returns:
        str:
        A greeting bye message.
    """
    am_pm = datetime.now().strftime("%p")  # current part of day (AM/PM)
    hour = datetime.now().strftime("%I")  # current hour
    day = datetime.now().strftime("%A")  # current day

    if am_pm == 'AM' and int(hour) < 10:
        exit_msg = f"Have a nice day, and happy {day}."
    elif am_pm == 'AM' and int(hour) >= 10:
        exit_msg = f"Enjoy your {day}."
    elif am_pm == 'PM' and (int(hour) == 12 or int(hour) < 3) and day in weekend:
        exit_msg = "Have a nice afternoon, and enjoy your weekend."
    elif am_pm == 'PM' and (int(hour) == 12 or int(hour) < 3):
        exit_msg = "Have a nice afternoon."
    elif am_pm == 'PM' and int(hour) < 6 and day in weekend:
        exit_msg = "Have a nice evening, and enjoy your weekend."
    elif am_pm == 'PM' and int(hour) < 6:
        exit_msg = "Have a nice evening."
    elif day in weekend:
        exit_msg = "Have a nice night, and enjoy your weekend."
    else:
        exit_msg = "Have a nice night."

    if event := celebrate():
        exit_msg += f'\nAnd by the way, happy {event}'

    return exit_msg
