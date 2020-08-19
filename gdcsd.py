#!/usr/bin/python3

copyright_msg = '''Geometry Dash Custom Song Downloader
Copyright (c) 2020 Sam L. Yes

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

home_url = "https://github.com/SamLukeYes/GDCSD"

import os, platform, time, sys

home = os.path.expanduser('~')
dl_config = f'{home}/.gdcsd_dl_dir'
tmp_dir = f'{home}/.cache/gdcsd'

if os.path.isfile(dl_config):   # if not exist, fall back to default
    dl_dir = open(dl_config).read()
elif platform.system() == 'Windows':
    dl_dir = f'{home}/AppData/Local/GeometryDash'
else:
    # for any other platform that uses Proton to run GD
    dl_dir = f'{home}/.local/share/Steam/steamapps/compatdata/322170/pfx/drive_c/users/steamuser/Local Settings/Application Data/GeometryDash'

def usage():
    print(f'''USAGE: {sys.argv[0]} <command> [args]
    
Defined commands:

    info            Display copyright infomation and current download directory
    dl              Download songs by ID and store them in custom song download directory
    set-dl-dir      Set custom song download directory, recommended to be the same as GD's
    help            Display this message
    
Other commands: Execute a system command in GD's custom song directory.
''')

def set_dl_dir(dir:str):
    if not os.path.isdir(dir):
        print(f'Invalid path: {dir}')
        sys.exit(1)
    path = os.path.abspath(dir)
    print(f'Writing to {dl_config}')
    with open(dl_config, 'w') as f:
        f.write(path)
    print(f'Custom song download directory set to {path}')

def join_args(arg_list:list):
    args = ''
    for arg in arg_list:
        args += arg + ' '
    return args[:-1]

def check_dl_dir():
    if not os.path.isdir(dl_dir):
        print(f"Error: {dl_dir} not exist")
        print(f"Please run '{sys.argv[0]} set-dl-dir <YOUR_GD_CUSTOM_SONG_PATH>'")
        sys.exit(1)

def mkdir(dir:str):
    if platform.system() == 'Windows':
        return os.system(f'powershell mkdir -p "{dir}"')
    else:
        return os.system(f'mkdir -p "{dir}"')

def rmdir(dir:str):
    if platform.system() == 'Windows':
        return os.system(f'rmdir /s /q "{dir}"')
    else:
        return os.system(f'rm -rf "{dir}"')

def multi_dl(targets:dict, ctrl_file:str, outdir:str):
    ctrl = ''
    for file_name in targets:
        ctrl += f'{targets[file_name]}\n out={file_name}\n'
    with open(ctrl_file, 'w') as f:
        f.write(ctrl)
    return os.system(f'aria2c -c -d "{outdir}" -i "{ctrl_file}"')

def dl(IDs:list):

    # Notes:
    #   For invoking, always use sys.exit()
    #   For editing this func itself, always rmdir(work_dir) before returning

    check_dl_dir()
    work_dir = f'{tmp_dir}/{time.time()}'
    mkdir(work_dir)
    os.chdir(work_dir)

    print('Fetching song info...')
    api_targets = dict()
    for id in IDs:
        if id.isdigit():
            api_targets[id] = f'https://api.newgrounds.app/details.php?url=https://www.newgrounds.com/audio/listen/{id}'
        else:
            raise ValueError(f'song ID {id} is invalid')
    code = multi_dl(api_targets, 'api.tmp', work_dir)
    if code:
        print('Failed to fetch song info.')
        rmdir(work_dir)
        return code
    
    print('Starting download...')
    mp3_targets = dict()
    for id in IDs:
        url = None
        data = open(id).read().split()
        for i in range(len(data)):
            if data[i] == '"media":':
                url = data[i+1].replace('"', '').replace('\\', '')
        if url:
            mp3_targets[f'{id}.mp3'] = url
        else:
            print(f'Failed to get download URL of {id}. Removing it from target list.')
            print(f"If you're sure it is a valid ID, please open an issue at {home_url}/issues")
            time.sleep(3)
    code = multi_dl(mp3_targets, 'songs.tmp', dl_dir)
    rmdir(work_dir)
    return code

def info():
    print(copyright_msg)
    print(f'Home page: {home_url}\n')
    print(f'Custom song download path: {dl_dir}\n')

if __name__ == '__main__':

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    elif sys.argv[1] == 'info':
        info()

    elif sys.argv[1] == 'dl':
        if len(sys.argv) == 2:
            print(f'USAGE: {sys.argv[0]} dl <ID1> [<ID2> <ID3> ...]')
            sys.exit(1)
        sys.exit(dl(sys.argv[2:]))

    elif sys.argv[1] == 'set-dl-dir':
        if len(sys.argv) == 2:
            print(f'USAGE: {sys.argv[0]} set-dl-dir <YOUR_GD_CUSTOM_SONG_PATH>')
            sys.exit(1)
        set_dl_dir(sys.argv[2])

    elif sys.argv[1] == 'help':
        usage()

    else:
        check_dl_dir()
        os.chdir(dl_dir)
        code = os.system(join_args(sys.argv[1:]))
        if code:
            print(f"Run '{sys.argv[0]} help' for help message.")