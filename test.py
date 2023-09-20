from pynput import keyboard

def on_key_press(key):
    try:
        # Print the key that was pressed
        print(f'Key pressed: {key.char}')

    except AttributeError:
        # Some keys don't have a char attribute (e.g., special keys)
        print(f'Special key pressed: {key}')

def on_key_release(key):
    # Print the key that was released
    print(f'Key released: {key}')

# Create a keyboard listener
listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)

# Start listening to keyboard events in the background
listener.start()

# Run the listener in the background
listener.join()
