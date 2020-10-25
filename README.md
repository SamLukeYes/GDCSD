# Geometry Dash Custom Song Downloader
A program aiming to accelerate Geometry Dash custom song downloading using Aria2

## Installation
### Windows
Download the [binary release](https://github.com/SamLukeYes/GDCSD/releases), extract it to any directory you like, and then add the directory to `PATH`.
You might also need [VCRUNTIME140](https://www.microsoft.com/en-us/download/details.aspx?id=52685) to run GDCSD binary. Remember to choose the x86 build.

### Linux
#### Arch-based distributions
    $ yay -S gdcsd-git
#### Other distributions
Make sure `aria2` is installed, and then

    $ git clone https://github.com/SamLukeYes/GDCSD
    # install -m755 GDCSD/gdcsd.py /usr/local/bin/gdcsd

## How to use

    USAGE: gdcsd <command> [args]
        
    Defined commands:

        info            Display copyright infomation and current download directory
        dl              Download songs by ID and store them in custom song download directory
        set             Set custom song download directory, recommended to be the same as GD's
        reset           Reset custom song download directory to default
        help            Display this message
        
    Other commands: Execute a system command in custom song download directory.