# Geometry Dash Custom Song Downloader
A program aiming to accelerate Geometry Dash custom song downloading using Aria2

## How to use
Before running GDCSD, please make sure you have installed [Python](https://python.org) (3.6 or higher) and [Aria2](https://aria2.github.io) properly.

For the first time to run or after an upgrade, please execute:

    chmod +x ./gdcsd.py  #for non-Windows users
    ./gdcsd.py init

Then the Python script will install `gdcsd.sh` and `controller.py` to `~/.local/share/gdcsd`. On Windows, there'll be `gdcsd.cmd` and `controller.py` in your user directory instead.

The shell script will be invoked for downloading and executing shell commands. I expect it to run out of box, but I haven't tested it on other devices, so please check them before downloading. If it doesn't work out of box on your device, please open an issue to discuss it.

    USAGE: ./gdcsd.py <command> [args]
    
    Commands:

        init            Set up the runtime environment
        dl              Download songs by their IDs and store them in GD's custom song directory
        help            Display this message
        
        Other commands: Run a shell command in GD's custom song directory (not available on Windows)

## Missing features
* GUI
* Checking duplicate song
* Downloading songs which don't have direct link, such as *Starchaser (ID: 689891)* -- it can be downloaded in the latest Geometry Dash, but I don't know how RubRub solved this problem
* Executing DOS commands on Windows
* Mobile device support
  
These features might be added if someone really needs them. New ideas and pull requests are also welcomed.