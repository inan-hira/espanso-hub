# Intended for use with the delays-characters package.yml file.
# Uses the Python pynput library to inject text, instead of Espanso. Enables the
# addition of pauses (sleep) and <Tab> etc. keys and can include Espanso {{variables}}
# See https://pynput.readthedocs.io/en/latest/keyboard.html#controlling-the-keyboard
# Supports type, tap, press, release, and sleep
#
# This script detaches itself into a background worker process before doing any
# typing, so that Espanso's "script" extension (which waits for the process to
# exit and for its stdout pipe to close) returns immediately instead of blocking
# for the duration of the sleeps/keystrokes.

import argparse, logging, os, subprocess, sys, time

WORKER_FLAG = '--worker'
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parse_pynput.log')

def launch_worker():
    """Relaunch this same script as a detached background process, then exit."""
    kwargs = {}
    if os.name == 'nt':
        # Fully detach on Windows: no console window, own process group.
        kwargs['creationflags'] = (
            subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        # POSIX: start a new session so it's detached from the controlling terminal.
        kwargs['start_new_session'] = True

    subprocess.Popen(
        [sys.executable, os.path.abspath(__file__), WORKER_FLAG, *sys.argv[1:]],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        **kwargs,
    )
    # Original process exits immediately; Espanso's wait() returns right away
    # with empty output, so {{Output}} resolves to "".
    sys.exit(0)

def parse_and_execute_commands(commands, keyboard, Key):
    lines = commands.strip().splitlines()

    for line in lines:
        line = line.strip()
        if line.startswith('type'):
            text = line[len('type '):].strip()
            keyboard.type(text)

        elif line.startswith('tap'):
            key_name = line[len('tap '):].strip().lower()
            key = getattr(Key, key_name, key_name)
            keyboard.tap(key)

        elif line.startswith('press'):
            key_name = line[len('press '):].strip().lower()
            key = getattr(Key, key_name, key_name)
            keyboard.press(key)

        elif line.startswith('release'):
            key_name = line[len('release '):].strip().lower()
            key = getattr(Key, key_name, key_name)
            keyboard.release(key)

        elif line.startswith('sleep'):
            time_to_sleep = float(line[len('sleep '):].strip())
            time.sleep(time_to_sleep)

def run_worker(input_text):
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
    )

    # Import pynput only in the worker process (also gives a clean error path
    # if it's missing, without affecting the fast-exiting launcher process).
    try:
        from pynput.keyboard import Controller, Key
    except ImportError:
        logging.error("The 'pynput' library is not installed. Install it using: pip install pynput")
        return

    keyboard = Controller()

    if input_text and input_text.strip():
        try:
            parse_and_execute_commands(input_text, keyboard, Key)
        except Exception:
            logging.exception("Error while executing input commands")
    else:
        logging.warning("No input provided.")

def main():
    parser = argparse.ArgumentParser(description="Execute keyboard automation commands.")
    parser.add_argument(WORKER_FLAG, action='store_true', help=argparse.SUPPRESS)
    parser.add_argument(
        'params',
        nargs='+',
        help='The input commands to execute. If two values are given '
             '(for backward compatibility with older package.yml files '
             'that also passed {{Trig}}), only the last one is used.',
    )
    args = parser.parse_args()

    # Support both the current package.yml (one positional: Input) and the
    # older one (two positionals: Trig, Input) -- always use the last value.
    input_text = args.params[-1]

    if args.worker:
        run_worker(input_text)
    else:
        launch_worker()

if __name__ == "__main__":
    main()
