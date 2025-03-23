import pygame
import time

def monitor_controllers(controller_ready):
    try:
        pygame.init()
        pygame.joystick.init()
        controller_ready.set()
        print("Monitoring for controller connections and disconnections...")

        connected_joysticks = {}

        while True:
            pygame.event.pump()  # Update the event queue

            try:
                current_joysticks = {
                    i: pygame.joystick.Joystick(i)
                    for i in range(pygame.joystick.get_count())
                }

                # Check for newly connected controllers
                for i, joystick in current_joysticks.items():
                    if i not in connected_joysticks:
                        joystick.init()
                        name = joystick.get_name()
                        if "360" in name:
                            continue
                        connected_joysticks[i] = joystick
                        print(f"Controller '{joystick.get_name()}' is connected!")

                # Check for disconnected controllers
                disconnected = [
                    i for i in connected_joysticks if i not in current_joysticks
                ]
                for i in disconnected:
                    print(f"Controller '{connected_joysticks[i].get_name()}' is disconnected.")
                    del connected_joysticks[i]

            except Exception as e:
                print(f"Error monitoring controllers: {e}")

            time.sleep(1)  # Avoid spamming the CPU

    except Exception as e:
        print(f"Failed to initialize controller monitoring: {e}")
