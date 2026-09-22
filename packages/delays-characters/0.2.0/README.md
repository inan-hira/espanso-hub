# Delays-characters

An Espanso trigger that uses the Python `pynput` library to inject text, *instead* of Espanso. This enables the addition of pauses (sleep), \<Tab> etc, and other key combinations not supported by Espanso. It can include use of Espanso {{variables}}. 

See https://pynput.readthedocs.io/en/latest/keyboard.html#controlling-the-keyboard for details of the keywords, and https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key for the key names.

If necessary, use `python3 -m pip install pynput` to add pynput to your Python 3 installation. Tested here with Python 3.10.

Supports keywords "type", "tap", "press", "release", and "sleep".

The package includes a sample script which demonstrates a delay and the effect of simulating depressing the \<Shift> key. For different scripts, copy and rename, the `package.yml` file into your `espanso/match/` directory. Edit the trigger value and Input list to suit your purpose.

v0.2.0 simplifies the Espanso trigger and removes the need to pass the trigger text to the Python script. It's backwardly compatible with your own edited trigger files, but you can now remove the `{{Trig}}` handling code from them if you wish.

A possible future enhancement could be the addition of mouse control.
