import yaml
import csv


class FilesEditor:

    def __init__(self, file_path, file_type, file_content=None):
        self.file_path = file_path
        self.file_content = file_content
        self.file_type = file_type

    def read_file(self):
        """The function reads the attribute's file based on the extension,
        and sets the content to the attribute"""
        with open(self.file_path, 'r') as read_file:
            if self.file_type == "yaml":
                config_content = yaml.full_load(read_file)
            else:
                config_content = []
                for row in read_file:
                    config_content.append(row)
            read_file.close()
        self.file_content = config_content

    def write_file(self):
        """The function writes this attribute content to this attribute file"""
        if self.file_type == "yaml":
            with open(self.file_path, 'w') as write_file:
                yaml.dump(self.file_content, write_file)
                write_file.close()

        if self.file_type == "csv":
            with open(self.file_path, 'a', newline='') as write_file:
                writer = csv.writer(write_file, dialect='excel')
                writer.writerow(self.file_content)
                write_file.close()
