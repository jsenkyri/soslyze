import re
from pathlib import Path


def print_headline(line):
    print((Style.NEW_LINE + Style.CYAN_BOLD + "{0}" + Style.RESET + Style.NEW_LINE).format(line))


def print_value(line, value):
    print((Style.BLUE_BOLD + "{0}" + Style.RESET_NEW_LINE +
           "{1}" + Style.NEW_LINE).format(line, value.rstrip()))


def package_present(path, name):
    result = False
    for line in Path(path + '/installed-rpms').read_text().splitlines():
        if re.search(r'^' + name + '.*', line):
            result = True
    return result


def parse_text(path, regex, options=0):
    lines = []
    try:
        for line in Path(path).read_text().splitlines():
            if re.search(regex, line, options):
                lines.append(line)
    except FileNotFoundError:
        pass
    return "\n".join(lines)


def parse_text_exclude(path, regex):
    lines = []
    try:
        for line in Path(path).read_text().splitlines():
            if not re.search(regex, line):
                lines.append(line)
    except FileNotFoundError:
        pass
    return "\n".join(lines)


class Style:
    GREY = '\033[0;90m'
    GREEN = '\033[0;32m'
    GREEN_BOLD = '\033[0;32m\033[1m'
    RED = '\033[0;31m'
    RED_BOLD = '\033[0;31m'
    YELLOW = '\033[01;33m'
    YELLOW_BOLD = '\033[01;33m\033[1m'
    BLUE = '\033[0;34m'
    BLUE_BOLD = '\033[0;34m\033[1m'
    CYAN = '\033[01;36m'
    CYAN_BOLD = '\033[01;36m\033[1m'
    PURPLE = '\033[0;35m'
    PURPLE_BOLD = '\033[0;35m\033[1m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    NEW_LINE = '\n'
    RESET_NEW_LINE = '\033[0m\n'
