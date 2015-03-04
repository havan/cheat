from cheat import cheatsheets
from cheat.utils import *
import os

def default_path():
    """ Returns the default cheatsheet path """

    # determine the default cheatsheet dir
    default_sheets_dir = os.environ.get('DEFAULT_CHEAT_DIR') or os.path.join(os.path.expanduser('~'), '.cheat')

    # create the DEFAULT_CHEAT_DIR if it does not exist
    if not os.path.isdir(default_sheets_dir):
        try:
            # @kludge: unclear on why this is necessary
            os.umask(0000)
            os.mkdir(default_sheets_dir)

        except OSError:
            die('Could not create DEFAULT_CHEAT_DIR')

    # assert that the DEFAULT_CHEAT_DIR is readable and writable
    if not os.access(default_sheets_dir, os.R_OK):
        die('The DEFAULT_CHEAT_DIR (' + default_sheets_dir +') is not readable.')
    if not os.access(default_sheets_dir, os.W_OK):
        die('The DEFAULT_CHEAT_DIR (' + default_sheets_dir +') is not writeable.')

    # return the default dir
    return default_sheets_dir


def get():
    """ Assembles a dictionary of cheatsheets as reldir/name => file-path """
    cheats = {}

    # Scan cheat paths and assemble a dictionary.
    # Cheats can be organized in subdirectories in cheat dirs.
    for cheat_dir in reversed(paths()):
        for root, subdirs, cheat_files in os.walk(cheat_dir):
            for cheat in cheat_files:
                cheat_path = os.path.join(root, cheat)
                cheat_name = os.path.relpath(os.path.join(root, cheat), cheat_dir)
                cheats[cheat_name] = cheat_path
    return cheats


def paths():
    """ Assembles a list of directories containing cheatsheets """
    sheet_paths = [
        default_path(),
        cheatsheets.sheets_dir()[0],
    ]

    # merge the CHEATPATH paths into the sheet_paths
    if 'CHEATPATH' in os.environ and os.environ['CHEATPATH']:
        for path in os.environ['CHEATPATH'].split(os.pathsep):
            if os.path.isdir(path):
                sheet_paths.append(path)

    if not sheet_paths:
        die('The DEFAULT_CHEAT_DIR dir does not exist or the CHEATPATH is not set.')

    return sheet_paths


def list():
    """ Lists the available cheatsheets """
    sheet_list = ''
    pad_length = max([len(x) for x in get().keys()]) + 4
    for sheet in sorted(get().items()):
        sheet_list += sheet[0].ljust(pad_length) + sheet[1] + "\n"
    return sheet_list


def search(term):
    """ Searches all cheatsheets for the specified term """
    result = ''

    for cheatsheet in sorted(get().items()):
        match = ''
        for line in open(cheatsheet[1]):
             if term in line:
                  match += '  ' + line

        if not match == '':
            result += cheatsheet[0] + ":\n" + match + "\n"

    return result
