import json
import os
import shutil
import tempfile
from datetime import datetime


class Backup:
    def __init__(self, config_filepath: str = "config.json") -> None:
        with open(config_filepath, encoding="utf-8") as config_file:
            self.config = json.load(config_file)

    def generate_output_archive_name(self) -> str:
        backup_name = self.config["backupNameTemplate"]
        now = datetime.now()
        backup_name = backup_name.replace("##DATE##", now.strftime("%Y-%m-%d"))
        backup_name = backup_name.replace("##TIME##", now.strftime("%H-%M-%S"))
        return backup_name

    def create_backup(self) -> None:
        print("Creating backup...")
        output_folder = self.config["backupsFolder"]
        os.makedirs(output_folder, exist_ok=True)

        output_archive_name = self.generate_output_archive_name()
        output_path = os.path.join(output_folder, output_archive_name)

        with tempfile.TemporaryDirectory() as temp_dir:
            for world in self.config["worldsToBackup"]:
                world_path = os.path.join(self.config["serverPath"], world)
                if os.path.exists(world_path):
                    shutil.copytree(world_path, os.path.join(temp_dir, world))
                else:
                    print(f"Warning: World folder '{world}' not found.")

            shutil.make_archive(
                output_path,
                self.config["backupFormat"],
                temp_dir,
            )

        full_archive_path = f"{output_path}.{self.config['backupFormat']}"
        print(f"Backup created at {full_archive_path}")
        print("Backup created successfully!")
