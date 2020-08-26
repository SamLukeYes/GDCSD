# Geometry Dash Custom Song Downloader
A program aiming to accelerate Geometry Dash custom song downloading using Aria2

## Installation
### Windows
#### 64-bit
Download the [release](https://github.com/SamLukeYes/GDCSD/releases/tag/20200821), extract it to any directory you like, and then add the directory to `PATH`.

#### 32-bit
Download a 32-bit release of Aria2 [here](https://github.com/aria2/aria2/releases) and add it to `PATH`. Install Python (3.6 or higher). You can choose to run `gdcsd.py` with Python (replace `gdcsd` command with `python path/to/gdcsd.py`), or compile it with PyInstaller and add it to `PATH`.

### Linux
#### Arch-based distributions
    yay -S gdcsd-git
#### Other distributions
Make sure `aria2` is installed, and then

    git clone https://github.com/SamLukeYes/GDCSD
    sudo install -m755 GDCSD/gdcsd.py /usr/local/bin/gdcsd

## How to use

    USAGE: gdcsd <command> [args]
        
    Defined commands:

        info            Display copyright infomation and current download directory
        dl              Download songs by ID and store them in custom song download directory
        set             Set custom song download directory, recommended to be the same as GD's
        reset           Reset custom song download directory to default
        help            Display this message
        
    Other commands: Execute a system command in custom song download directory.