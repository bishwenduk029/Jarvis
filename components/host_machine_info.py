from platform import platform
from shutil import disk_usage

from psutil import cpu_count, virtual_memory

from components.convert_bytes import size_converter


def system_info() -> str:
    """Gets the system configuration.

    Returns:
        str:
        A compiled version of all required system information as a string.
    """
    total, used, free = disk_usage("/")
    total = size_converter(total)
    used = size_converter(used)
    free = size_converter(free)
    ram = size_converter(virtual_memory().total).replace('.0', '')
    ram_used = size_converter(virtual_memory().percent).replace(' B', ' %')
    physical = cpu_count(logical=False)
    logical = cpu_count(logical=True)
    o_system = platform().split('.')[0]
    return f"You're running {o_system}, with {physical} physical cores and {logical} logical cores. " \
           f"Your physical drive capacity is {total}. You have used up {used} of space. Your free space is " \
           f"{free}. Your RAM capacity is {ram}. You are currently utilizing {ram_used} of your memory."
