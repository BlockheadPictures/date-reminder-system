import datetime
import time
import os
import json
from pathlib import Path
import subprocess

class ReminderSystem:
    def __init__(self):
        self.reminders_file = Path.home() / "reminders.json"
        self.reminders = self.load_reminders()

    def load_reminders(self):
        if self.reminders_file.exists():
            with open(self.reminders_file, 'r') as f:
                return json.load(f)
        return {}

    def save_reminders(self):
        with open(self.reminders_file, 'w') as f:
            json.dump(self.reminders, f)

    def add_reminder(self, date, message, phone_number):
        if date not in self.reminders:
            self.reminders[date] = []
        self.reminders[date].append({
            'message': message,
            'phone_number': phone_number
        })
        self.save_reminders()

    def send_message(self, phone_number, message):
        applescript = f'''
        tell application "Messages"
            send "{message}" to buddy "{phone_number}" of (service 1 whose service type is iMessage)
        end tell
        '''
        subprocess.run(['osascript', '-e', applescript])

    def check_reminders(self):
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        if today in self.reminders:
            for reminder in self.reminders[today]:
                self.send_message(
                    reminder['phone_number'],
                    reminder['message']
                )

def main():
    reminder_system = ReminderSystem()
    
    while True:
        print("\n1. Add new reminder")
        print("2. View all reminders")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ")
            message = input("Enter reminder message: ")
            phone = input("Enter your phone number: ")
            reminder_system.add_reminder(date, message, phone)
            print("Reminder added successfully!")
            
        elif choice == "2":
            print("\nAll reminders:")
            for date, reminders in reminder_system.reminders.items():
                for reminder in reminders:
                    print(f"Date: {date}")
                    print(f"Message: {reminder['message']}")
                    print(f"Phone: {reminder['phone_number']}")
                    print("---")
                    
        elif choice == "3":
            break

if __name__ == "__main__":
    main()
