import controller as controller
import pygame
import pygetwindow as gw
import threading
import time
import os
import pyautogui

def find_playnite_window():
    windows = gw.getWindowsWithTitle("Playnite")
    return windows[0] if windows else None

def wait_for_playnite():
    while True:
        try:
            window = find_playnite_window()
            if window:
                break
        except Exception as e:
            print(f"Waiting for Playnite... (error: {e})")
        time.sleep(1)

def start_playnite():
    path = r"C:\Users\20128\AppData\Local\Playnite\Playnite.FullscreenApp.exe"
    os.startfile(path)
    wait_for_playnite()
    window = find_playnite_window()
    window.activate()

def handle_ps_button():
    window = find_playnite_window()
    if not window:
        start_playnite()
    else:
        window = gw.getActiveWindow()
        window.activate()
        pyautogui.hotkey('alt', 'f4')

IGNORED_NAMES = ["xbox 360", "xinput"]

def is_ignored_controller(joy_id):
    name = pygame.joystick.Joystick(joy_id).get_name().lower()
    return any(ignored in name for ignored in IGNORED_NAMES)

def main():
    PS_BUTTON = 5

    controller_ready = threading.Event()
    controller_thread = threading.Thread(
        target=controller.monitor_controllers,
        args=(controller_ready,),
        daemon=True)

    controller_thread.start()
    controller_ready.wait()

    try:
        while True:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN:

                        if is_ignored_controller(event.joy):
                            continue  # ❌ Ignore this controller

                        if event.button == PS_BUTTON:
                            handle_ps_button()
                time.sleep(0.005)
            except Exception as e:
                print(f"Error in event loop: {e}")
                time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting program.")

    except Exception as e:
        print(f"Main loop error: {e}")

if __name__ == "__main__":
    main()
