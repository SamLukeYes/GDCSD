# Geometry Dash Custom Song Downloader
A script aiming to accelerate Geometry Dash custom song downloading using [Aria2](http://aria2.github.io)

## Installation
### Windows
The binary releases for Windows are not maintained currently, because I only use GDCSD on Linux and don't want to test it on Windows. To use it on Windows, you are on your own to get the Python script work. Pull requests for Windows compatability are welcomed.

### Linux
#### Arch-based distro

    $ yay -S gdcsd-git

#### Other distro

    $ git clone https://github.com/SamLukeYes/GDCSD
    # install -m755 GDCSD/gdcsd.py /usr/local/bin/gdcsd

## How to use

    USAGE: gdcsd <subcommand> [args]
        
    Subcommands:

        info            Display copyright infomation
        dir             Print the current download directory
        dl              Download songs to custom song download directory
        set             Set custom song download directory
        reset           Reset custom song download directory to default
        help            Display this message