## File Renamer

### Instructions

#### Installation
Install Python3 from the python [website](https://www.python.org/downloads/release/python-352/)
P.S. - It's probably [this one](https://www.python.org/ftp/python/3.5.2/python-3.5.2-amd64.exe)

Copy file_renamer.py into the directory containing the files you want to rename.

#### Running the script
Open a command prompt window and cd into the directory with all the files and the script.
Run the command by typing `python3 file_renamer.py`

There are two modes, one where the magic prefix files are skipped (default) and one where they aren't. If you want to not skip just add `--no-skip-prefix` or `-n` to the command prompt line
If you need help, you can also type `file_renamer.py --help` at any time

#### Runtime Instructions
Follow the prompts, obviously. When you are in the flow of the program, you have a couple of "special" control flow commands you can issue.
`\help` or `\?` will print out the available commands (`\` is not an allowed filename character in Windows, FYI). Basically, you can `\skip` a file,
use `\back` to go back to the previous file, or `\exit` to exit.

### Contact
If you need anything, I'm making myself contractually obligated to provide support to any questions or issues within 1 business day or before A&M wins another game (in football) whichever is greater. So this should be a good opportunity to read the source code and fix any bugs yourself!