import os
import shutil

def main():
    public_dir_path = "/home/khaledoti/workspace/github.com/Khalid-oti/static_site/public"
    static_dir_path = "/home/khaledoti/workspace/github.com/Khalid-oti/static_site/static"
    if not os.path.exists(public_dir_path):
        raise Exception("path does not exist")
    shutil.rmtree(public_dir_path)
    os.mkdir(public_dir_path)
    copy_dir(static_dir_path, public_dir_path)

def copy_dir(source_dir_path, destination_dir_path):
    dir_content_path_list = os.listdir(source_dir_path)
    for content in dir_content_path_list:
        content_path = f"{source_dir_path}/{content}"
        if os.path.isfile(content_path):
            shutil.copy(content_path, destination_dir_path)
        if os.path.isdir(content_path):
            new_destination_dir_path = f"{destination_dir_path}/{content}"
            os.mkdir(new_destination_dir_path)
            copy_dir(content_path, new_destination_dir_path)
        if not os.path.isfile(content_path) and not os.path.isdir(content_path):
            raise Exception("path does not exist")

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.strip()[0:2] == "# ":
            return line.strip()[2:]
    raise Exception("no title")
        
main()
