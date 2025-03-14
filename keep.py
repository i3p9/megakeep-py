import os
import time
import subprocess
from datetime import datetime
import random

class MegaKeep:
    def __init__(self, txt_file_path):
        self.txt_file_path = txt_file_path
        self.log_file_path = f"logs/{datetime.now().strftime('%Y%m%d-%H%M%S')}-log.txt"

    def log(self, message):
        timestamp = f"[{datetime.now().strftime('%H:%M:%S')}] "
        log_entry = f"{timestamp}{message}\n"
        print(log_entry, end="")
        with open(self.log_file_path, "a") as log_file:
            log_file.write(log_entry)

    def validate_txt_file(self):
        if not os.path.exists(self.txt_file_path) or not self.txt_file_path.endswith(
            ".txt"
        ):
            self.log("The file could not be found or is not a .txt file.")
            return False
        return True

    def read_lines(self):
        try:
            with open(self.txt_file_path, "r") as file:
                return file.readlines()
        except Exception as e:
            self.log(f"Error reading file: {e}")
            return []

    def run_process(self, command, arguments):
        try:
            full_command = [command, *arguments]
            result = subprocess.run(full_command, capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            self.log(f"Error running process {command}: {e}")
            return ""

    def login(self, user, password):
        self.log(f"Logging in as: {user}")
        return self.run_process("mega-login", [f'"{user}"', f'"{password}"'])

    def size(self,user):
        self.log(f"Getting usage: {user}")
        output = self.run_process("mega-df", [f'-h'])

        for line in output.splitlines():
            if "USED STORAGE:" in line:
                cleaned_line = ' '.join(word for word in line.split() if word)
                return cleaned_line

        return output

    def logout(self):
        self.log("Logging out...")
        return self.run_process("mega-logout", [])

    def whoami(self):
        #return stirng: Account e-mail: email@domain.com
        output = self.run_process("mega-whoami", [])
        for line in output.splitlines():
            if "Account e-mail:" in line:
                return line.split(":")[1].strip()
        return ""

    def process_accounts(self):
        if not self.validate_txt_file():
            return

        lines = self.read_lines()
        self.logout()

        total_accounts = len(lines)
        successful_logins = 0
        failed_logins = 0
        successful_size_checks = 0

        self.log(f"Starting to process {total_accounts} accounts")

        for line in lines:
            line = line.strip()
            if ":" not in line:
                self.log(f"Invalid format (missing colon): {line}")
                failed_logins += 1
                continue

            user, password = line.split(":", 1)
            time.sleep(random.randint(5, 7))

            login_success = False

            for attempt in range(2):
                self.login(user, password)

                time.sleep(random.randint(2, 3))
                whoami = self.whoami()
                if whoami == user:
                    self.log(f"Logged in as: {user}")

                time.sleep(random.randint(2, 3))
                size = self.size(user)
                if 'USED STORAGE:' in size:
                    self.log(f"Usage for {user}: {size}")
                    login_success = True
                    successful_size_checks += 1
                    break
                else:
                    self.log(f"Error getting usage for {user}: {size}")

                time.sleep(random.randint(5, 7))

            if login_success:
                successful_logins += 1
            else:
                failed_logins += 1

            self.logout()
            time.sleep(random.randint(5, 7))

        self.log("\n===== SUMMARY =====")
        self.log(f"Total accounts processed: {total_accounts}")
        self.log(f"Successful logins: {successful_logins} ({successful_logins/total_accounts*100:.2f}%)")
        self.log(f"Failed logins: {failed_logins} ({failed_logins/total_accounts*100:.2f}%)")
        self.log(f"Successful size checks: {successful_size_checks} ({successful_size_checks/total_accounts*100:.2f}%)")
        self.log("===================")

        self.log("Processing completed.")


def main():
    txt_file_path = "accounts_example.txt"
    mega_keep = MegaKeep(txt_file_path)
    mega_keep.process_accounts()


if __name__ == "__main__":
    main()
