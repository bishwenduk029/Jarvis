from datetime import datetime


def part_of_day() -> str:
    """Checks the current hour to determine the part of day.

    Returns:
        str:
        Morning, Afternoon, Evening or Night based on time of day.
    """
    am_pm = datetime.now().strftime("%p")
    current_hour = int(datetime.now().strftime("%I"))
    if current_hour in range(4, 12) and am_pm == 'AM':
        greet = 'Morning'
    elif am_pm == 'PM' and (current_hour == 12 or current_hour in range(1, 4)):
        greet = 'Afternoon'
    elif current_hour in range(4, 8) and am_pm == 'PM':
        greet = 'Evening'
    else:
        greet = 'Night'
    return greet
