import json
import os
import time

from backup import Backup


class App:

    def __init__(self) -> None:
        if not os.path.exists("config.json"):
            raise FileNotFoundError("Configuration file not found.")

        self.update_config()

    def update_config(self) -> None:
        if not os.path.exists("config.json"):
            raise FileNotFoundError("Configuration file not found.")
        with open("config.json", encoding="utf-8") as config_file:
            self.config = json.load(config_file)

    def clean_backups(self) -> None:
        backup_files = os.listdir(self.config["backupsFolder"])
        if len(backup_files) <= self.config["maxBackupCount"]:
            return

        backup_files.sort(
            key=lambda x: os.path.getmtime(
                os.path.join(self.config["backupsFolder"], x)
            )
        )
        for file in backup_files[: len(backup_files) - self.config["maxBackupCount"]]:
            os.remove(os.path.join(self.config["backupsFolder"], file))

    def create_backup(self) -> None:
        if not os.path.exists(self.config["serverPath"]):
            raise FileNotFoundError("Server folder not found.")
        if not os.path.exists(self.config["backupsFolder"]):
            os.makedirs(self.config["backupsFolder"], exist_ok=True)

        backup = Backup()
        backup.create_backup()

    def run(self) -> None:
        if not os.path.exists(self.config["serverPath"]):
            raise FileNotFoundError("Server folder not found.")

        if not os.path.exists(self.config["backupsFolder"]):
            os.makedirs(self.config["backupsFolder"], exist_ok=True)

        if self.config["backupOnStart"]:
            self.create_backup()

        while True:
            self.clean_backups()
            time.sleep(self.config["backupInterval"])
            self.create_backup()


if __name__ == "__main__":
    app = App()
    app.run()
