#!/usr/bin/python3

copyright_msg = '''Geometry Dash Custom Song Downloader
Copyright (c) 2020-2021 Sam L. Yes

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

Home Page: <https://github.com/SamLukeYes/GDCSD>'''

import os, platform, time, sys
from urllib.request import urlopen

home = os.path.expanduser('~')
dl_config = f'{home}/.gdcsd_dl_dir'

def get_dl_dir():
    if os.path.isfile(dl_config):   # if not exist, fall back to default
        return open(dl_config).read()
    elif platform.system() == 'Windows':
        return f'{home}/AppData/Local/GeometryDash'
    else:
        # for any other platform that uses Proton to run GD
        return f'{home}/.local/share/Steam/steamapps/compatdata/322170/pfx/drive_c/users/steamuser/Local Settings/Application Data/GeometryDash'

dl_dir = get_dl_dir()

def usage():
    print(f'''USAGE: {sys.argv[0]} <subcommand> [args]
    
Subcommands:

    info            Display copyright infomation
    dir             Print the current download directory
    dl              Download songs to custom song download directory
    set             Set custom song download directory
    reset           Reset custom song download directory to default
    help            Display this message''')

def set_dl_dir(dir:str):
    check_dl_dir(dir)
    path = os.path.abspath(dir)
    #print(f'Writing to {dl_config}')
    with open(dl_config, 'w') as f:
        f.write(path)
    print(f'Custom song download directory set to {path}')

def join_args(arg_list:list):
    args = ''
    for arg in arg_list:
        args += arg + ' '
    return args[:-1]

def check_dl_dir(dir=dl_dir):
    if not os.path.isdir(dir):
        print(f'Invalid path: {dir}')
        sys.exit(1)

def mkdir(target_dir:str) -> int:
    if not os.path.isdir(target_dir):
        if platform.system() == 'Windows':
            target_dir = target_dir.replace("/", "\\")
            return os.system(f'mkdir "{target_dir}"')
        else:
            return os.system(f'mkdir -p "{target_dir}"')
    return 0

def rmdir(target_dir:str) -> int:
    if platform.system() == 'Windows':
        return os.system(f'rmdir /s /q "{target_dir}"')
    else:
        return os.system(f'rm -rf "{target_dir}"')

def multi_dl(targets:dict, outdir:str) -> int:
    if platform.system() == 'Windows':
        tmp_dir = f'{home}/Temp/gdcsd'
    else:
        tmp_dir = '/tmp/gdcsd'
    mkdir(tmp_dir)
    control_file = f'{tmp_dir}/{time.time()}'
    control = ''
    for file_name in targets:
        control += f'{targets[file_name]}\n out={file_name}\n'
    with open(control_file, 'w') as f:
        f.write(control)
    code = os.system(f'aria2c -c -d "{outdir}" -i "{control_file}"')
    os.remove(control_file)
    return code

def get_url(id):
    target = 'embedController([{"url":"'
    with urlopen(f'https://www.newgrounds.com/audio/listen/{id}') as f:
        for i in f:
            line = str(i)
            if target in line:
                for j in line.split():
                    if target in j:
                        url=''
                        for k in str(j[len(target):]):
                            if k == '\\':
                                continue
                            if k == '?':
                                return url
                            else:
                                url += k
                        
                

def dl(IDs:list) -> int:

    # NOTE: always use sys.exit() when invoking

    check_dl_dir()
    
    print('Preparing to download...')
    mp3_targets = dict()
    for id in IDs:
        if id.isdigit():
            url = get_url(id)
        else:
            raise ValueError(f'song ID {id} is invalid')
        if url:
            mp3_targets[f'{id}.mp3'] = url
        else:
            print(f'Failed to get download URL of {id}.')
            sys.exit(1)
    code = multi_dl(mp3_targets, dl_dir)
    #rmdir(work_dir)
    return code

def reset():
    if os.path.isfile(dl_config):
        os.remove(dl_config)
    print(f'Custom song download directory set to {get_dl_dir()}')

if __name__ == '__main__':

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    elif sys.argv[1] == 'info':
        print(copyright_msg)

    elif sys.argv[1] == 'dir':
        print(dl_dir)

    elif sys.argv[1] == 'dl':
        if len(sys.argv) == 2:
            print(f'USAGE: {sys.argv[0]} dl <ID1> [<ID2> <ID3> ...]')
            sys.exit(1)
        sys.exit(dl(sys.argv[2:]))

    elif sys.argv[1] == 'set':
        if len(sys.argv) == 2:
            print(f'USAGE: {sys.argv[0]} set <CUSTOM_SONG_PATH>')
            sys.exit(1)
        set_dl_dir(sys.argv[2])

    # elif sys.argv[1] == 'clean':
    #     clean()

    elif sys.argv[1] == 'reset':
        reset()

    elif sys.argv[1] == 'help':
        usage()

    else:
        usage()
        sys.exit(1)

        # DEPRECATED: run any commands in dl_dir
        # check_dl_dir()
        # os.chdir(dl_dir)
        # code = os.system(join_args(sys.argv[1:]))
        # if code:
        #     print(f"Run '{sys.argv[0]} help' for help message.")
        #     print(code)
        #     sys.exit(code)