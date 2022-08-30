"""
The purpose of this project is to functionally turn Obsidian into a Markdown editor.
Right now, you can only edit files in your vault.
This shouldn't be too hard to change.

Author: Ronik
"""

import os
import argparse
import shutil
import re

TEMP_DIR_NAME = "Editor"
PATH_TO_VAULT = "/Users/ronikbhaskar/Documents/Vault"
PATH_TO_TEMP = os.path.join(PATH_TO_VAULT, TEMP_DIR_NAME)
PATH_TO_IMAGES = os.path.join(PATH_TO_VAULT, "Files")
VALID_MD_EXTS = [".md"]
OBSIDIAN_IMAGE_FORMAT = r"(!\[\[)([^\]]+)(\]\])"
VALID_IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".svg", ".gif", ".tif", ".tiff"]

def confirm(message):
    print(message)
    while 1:
        inp = input("y/n: ")
        if len(inp) > 0 and inp[0].lower() in {"y", "n"}:
            return inp[0].lower() == "y"

def setup(args):
    """
    checks state of obsidian editor and validity of arguments
    creates obsidian editor environment
    """

    # Obsidian only deals in markdown files
    extension = os.path.splitext(args.path)[1]
    if extension not in VALID_MD_EXTS:
        print("Invalid path extension.")
        exit(0)
    
    if not os.path.isabs(args.path):
        args.path = os.path.join(os.getcwd(), args.path)

    name = os.path.basename(args.path)
    directory = os.path.dirname(args.path)

    # directory should exist AND directory cannot be the one we are about to delete
    if not os.path.exists(directory) or PATH_TO_VAULT in directory:
        print("Invalid directory")
        exit(0)

    # double check that we should clear the editor
    if args.delete_editor and os.path.exists(PATH_TO_TEMP):
        if not confirm(f"WARNING: {PATH_TO_TEMP} still exists. Are you sure you want to delete it?"):
            exit(0)
        shutil.rmtree(PATH_TO_TEMP)
    
    # make temp folder
    if not os.path.exists(PATH_TO_TEMP):
        os.mkdir(PATH_TO_TEMP)

    temp_file = os.path.join(PATH_TO_TEMP, name)
    if os.path.exists(temp_file):
        if not confirm(f"WARNING: {temp_file} already exists in editor. Are you sure you want to overwrite it?"):
            exit(0)
    
     # Important to note that any linked resources in the Markdown file are not copied
    if os.path.exists(args.path):
        shutil.copy(args.path, temp_file)
    else:
        # open and close file to create it, like the touch command
        with open(temp_file, "w") as f:
            pass

    # this won't actually open the file in Obsidian, but it will open Obsidian
    # I could scrap the temp_file arg, but it seems to prevent some bugs when opening Obsidian like this
    os.system(f"open {temp_file} -a Obsidian")

    return name, temp_file

def cleanup(name, temp_file, args):
    """
    make the necessary changes to reformat the images
    copy over the file and all linked images
    """

    with open(temp_file, "r") as f:
        text = f.read()

    images = []

    def reformat(m):
        for ext in VALID_IMAGE_EXTS:
            if m.group(2).endswith(ext):
                images.append(m.group(2))
                return "![](" + m.group(2) + ")"
        # ignore linking to PDFs or other Markdown files
        else:
            return m.group()
        
    text = re.sub(OBSIDIAN_IMAGE_FORMAT, reformat, text)

    # if there are any images
    if len(images) > 0:
        directory = os.path.dirname(args.path)

        name_no_spaces = re.sub(r"\?", "", re.sub(r"\s", "_", name))

        resources_dir = os.path.join(directory, name_no_spaces + "_resources")
        if not os.path.exists(resources_dir):
            os.mkdir(resources_dir)

        for i, image in enumerate(images):
            extension = os.path.splitext(image)[1]
            new_image = f"img{i}{extension}"
            new_image_path = os.path.join(resources_dir, new_image)
            if not os.path.exists(new_image_path):
                # strong assumption that image is stored where expected
                shutil.copy(os.path.join(PATH_TO_IMAGES, image), 
                            new_image_path)

            text = re.sub(image, f"{name_no_spaces}_resources/{new_image}", text)

    with open(args.path, "w") as f:
        f.write(text)

    # double check that we should clear the editor again
    if args.delete_editor and os.path.exists(PATH_TO_TEMP):
        if not confirm(f"WARNING: {PATH_TO_TEMP} will be removed. Are you sure you want to delete it?"):
            exit(0)
        shutil.rmtree(PATH_TO_TEMP)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to Markdown file required")
    parser.add_argument("-d", "--delete-editor", help="flag to delete editor environment", action="store_true")
    args = parser.parse_args()

    name, temp_file = setup(args)

    input("Press Enter when finished: ")

    cleanup(name, temp_file, args)

if __name__ == "__main__":
    main()
