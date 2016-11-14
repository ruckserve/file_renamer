#!/usr/bin/env python3

import os
import argparse

class FileRenamer() :
    def __init__(self) :
        self.topdir = os.getcwd()
        self.file_prefix = self.get_file_prefix()

    def print_header(self, header, fill_char="="):
        # Pad with spaces
        header = " {} ".format(header.strip())
        # Header 90 chars accross, first 10 header then title then fill right to 80
        print("\n{fill:{fill}<10}{head:{fill}<80}".format(fill=fill_char, head=header))

    def get_file_prefix(self) :
        while True :
            self.print_header("FILE PREFIX", "/")
            file_prefix = input("Enter the file prefix: ")
            confirmation = input("Prefix all files with '{}' (y/n)? ".format(file_prefix))
            confirmed = confirmation.upper().strip().startswith("Y")
            if confirmed :
                return file_prefix

    def all_files(self, skip) :
        for root, dirs, files in os.walk(self.topdir) :
            for file in files :
                # Exclude this script and the README, obviously
                if file == __file__ or file == "README.md" or file == "README.html" :
                    continue
                # If user hasn't passed --no-skip, we don't want to rename files that have
                # already been renamed
                if skip and file.startswith(self.file_prefix) :
                    continue

                # Get what follows the last dot as the file extension
                file_extension = "." + file.split(".")[-1]
                yield root, file, file_extension

    def prompt_for_new_filename(self, root, filename, no_control=False):
        self.print_header(os.path.join(root, filename))
        return input("Input new name for file '{}' (\\? for help): ".format(filename))

    def control_statement(self, command_in, previous_file=None) :
        available_commands = ["help", "?", "skip", "exit"]
        if previous_file :
            available_commands.append("back")

        # Sanitize input
        command = command_in.strip().lstrip("\\").lower()
        if command not in available_commands :
            print("/{} is not an allowed command".format(command))
        elif command == "help" or command == "?" :
            self.print_help(available_commands)
        elif command == "exit" :
            print("\nGoodbye")
            exit()
        elif command == "back" :
            previous_root, previous_filename, previous_extension, current_name = previous_file
            while True :
                user_input = self.prompt_for_new_filename(previous_root, previous_filename)
                if "\\" in user_input :
                    cmd = self.control_statement(user_input)
                    if cmd == "skip" :
                        # We'll need to put the file back the way it was
                        user_input = previous_filename
                        break
                    continue
                if self.rename_file(previous_root, current_name, user_input, previous_extension) :
                    break
        else :
            # Nothing to do for skip command here
            pass
        return command

    def print_help(self, available_commands) :
        all_commands = {
            "help" : "\\help or \\? Print this menu and continue",
            "skip" : "\\skip       Skip renaming this file",
            "exit" : "\\exit       Exit the program",
            "back" : "\\back       Go back to the previous file and rename again"
        }
        available_commands.remove("?")   # Remove duplicate help command
        for command in available_commands :
            print("     {}".format(all_commands.get(command)))

    def run(self, skip=True) :
        previous_file = None
        for root, filename, file_extension in self.all_files(skip) :
            while True :
                user_input = self.prompt_for_new_filename(root, filename)

                # Handle input of a control statement
                if "\\" in user_input :
                    if self.control_statement(user_input, previous_file) == "skip" :
                        break
                    continue

                if self.rename_file(root, filename, user_input, file_extension) :
                    break

    def rename_file(self, root, curr_name, new_name, extension) :
        if "\\" in new_name :
            raise ValueError("\\ is not a valid filename character")

        # Prepend prefix and append extension. Don't append extensions if user already put it in there
        if not new_name.endswith(extension) :
            new_name = new_name + extension
        new_filename = self.file_prefix + new_name

        old_path = os.path.join(root, curr_name)
        new_path = os.path.join(root, new_filename)

        try :
            os.rename(old_path, new_path)
        except OSError as e :
            print("Filename already exists - {}".format(e.message))
            return False
        return True


if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--no-skip-prefix", default=False, action="store_true",
                        help="Rename all files, even if they already have the desired prefix")
    args = parser.parse_args()
    skip = not args.no_skip_prefix

    file_renamer = FileRenamer()
    file_renamer.run(skip)
