import os
import shutil
import sys
from markdown import markdown_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

def main():
    public_dir_path = "/home/khaledoti/workspace/github.com/Khalid-oti/static_site/public"
    static_dir_path = "/home/khaledoti/workspace/github.com/Khalid-oti/static_site/static"
    basepath = sys.argv
    if not os.path.exists(public_dir_path):
        raise Exception("path does not exist")
    shutil.rmtree(public_dir_path)
    os.mkdir(public_dir_path)
    copy_dir(static_dir_path, public_dir_path)
    generate_path_recursive(basepath)

def generate_path_recursive(basepath):
    for current_path, dirnames, filenames in os.walk("content"):
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            from_filepath = os.path.join(current_path, filename)
            relative_path = os.path.relpath(current_path, "content")
            dest_filepath = os.path.join("public", relative_path, name + ".html")
            generate_path(from_filepath, "template.html", dest_filepath, basepath)

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

def generate_path(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path}  using {template_path}")
    with open(from_path) as f:
        from_content = f.read()
    with open(template_path) as g:
        template_content = g.read()
    html = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)
    template_with_title = template_content.replace("{{ Title }}", title)
    template_with_content = template_with_title.replace("{{ Content }}", html)
    templatev3 = template_with_content.replace('href="/', f'href="{basepath}')
    filled_template = templatev3.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as h:
        h.write(filled_template)


main()
