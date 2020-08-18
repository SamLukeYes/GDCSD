#!/usr/bin/python

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

import sys, os, platform, time

home = os.path.expanduser('~')
#install_path = f'{home}/.local/share/gdcsd'
url = 'https://newgrounds.com/audio/download/'
dl_dir = 'Local Settings/Application Data/GeometryDash'

if platform.system() == 'Windows':
    script_type = 'cmd'
    install_path = home
    dl_dir = f'{home}/{dl_dir}'
else:
    script_type = 'sh'
    install_path = f'{home}/.local/share/gdcsd'
    dl_dir = f'{home}/.local/share/Steam/steamapps/compatdata/322170/pfx/drive_c/users/steamuser/{dl_dir}'

# def detect_downloader():

#     for downloader in ['aria2c', 'axel', 'curl', 'wget']:
#         if os.system(f'{downloader} --version') == 0:
#             return downloader

def create_controller(controller):
    with open(controller, 'w') as script:
        script.write(
f'''#!/usr/bin/python3
from sys import argv
for id in argv[1:]:
    print('{url}/'+id)
    print(" out="+id+".mp3")'''
    )

def install():

    controller = f'{install_path}/controller.py'

    if platform.system() == 'Windows':
        os.system(f'mkdir /p "{install_path}"')
        with open(f'{install_path}/gdcsd.{script_type}', 'w') as script:
            script.write(f'python {controller} %* > "{install_path}/ngdl.lst"\naria2c -c -d "{dl_dir}" -i "{install_path}/ngdl.lst"')
        #os.system(f'setx path %path%;{install_path}')
        create_controller(controller)

    else:
        os.system(f'mkdir -p "{install_path}"')
        os.chdir(install_path)
        with open(f'gdcsd.{script_type}', 'w') as script:
            script.write(f'#!/bin/sh\ndl_dir="{dl_dir}"\n{controller} $@ | aria2c -c -d "$dl_dir" -i -')
        create_controller(controller)
        os.system('chmod +x *')

def init():

    #downloader = detect_downloader()
    print(copyright_msg)

    #dl_dir = 'Local Settings/Application Data/GeometryDash'
    
    #if platform.system() == 'Windows':
        #dl_dir = f'{home}/{dl_dir}'
        #script_type = 'cmd'
    #else:
        #dl_dir = f'{home}/.local/share/Steam/steamapps/compatdata/322170/pfx/drive_c/users/steamuser/{dl_dir}'
        #script_type = 'sh'

    install()
    print('Checking if Aria2 is available...')
    time.sleep(1)

    if os.system('aria2c -v'):
        print(f'Aria2 not detected! Please edit {install_path}/gdcsd.{script_type} manually.')
        #found_aria2 = False
    #else:
        #found_aria2 = True

    print(f'\nDownload directory is set to {dl_dir}')
    print(f'If it is incorrect, please edit {install_path}/gdcsd.{script_type} manually.')


def how_to_use():
    print(f'''USAGE: {sys.argv[0]} <command> [args]
    
Commands:

    init            Set up the runtime environment
    dl              Download songs by ID and store them in GD's custom song directory
    help            Display this message
    
    Other commands: Run a shell command in GD's custom song directory (not available on Windows)
    ''')
    #sys.exit(1)

def dl(args):

    argstr = ''
    for id in args:
        if id.isdigit():
            argstr += f'{id} '
        else:
            #print(f'Invalid argument: {id}\n')
            #how_to_use()
            #sys.exit(1)
            raise ValueError(f'invalid song ID {id}')

    exit_code = os.system(f'{install_path}/gdcsd.{script_type} {argstr}')
    if exit_code:
        
        #sys.exit(exit_code)
        return exit_code

    for id in args:
        target = f'{dl_dir}/{id}.mp3'
        try:
            with open(target) as f:
                f.read()
            #os.remove(target)
            print(f'{id}.mp3 doesn\'t seem to be a valid mp3 file.')
            print(f'Try visiting https://newgrownds.com/audio/listen/{id} to download it manually.')
        except UnicodeDecodeError:
            pass

    return 0

if __name__ == '__main__':

    if len(sys.argv) < 2:
        how_to_use()
        sys.exit(1)

    elif sys.argv[1] == 'init':
        init()

    elif sys.argv[1] in ('help', '-h', '--help', '-?' '/help', '/h', '/?'):
        how_to_use()

    elif not os.path.isfile(f'{install_path}/gdcsd.{script_type}'):
        print(f'Please run "{sys.argv[0]} init" first.')

    elif sys.argv[1] == 'dl':
        if dl(sys.argv[2:]):
            print(f'Command failed for unknown reason. Run "{sys.argv[0]} init" to fix it?')

    elif platform.system == 'Windows':
        print('Custom command is not yet available on Windows.')

    else:
        with open(f'{install_path}/gdcsd.sh') as script:
            target = 'dl_dir='
            for line in script:
                if line.startswith(target):
                    dl_dir = line[len(target):-1].replace('"', '')
                    #break
        os.chdir(dl_dir)
        cmd = ''
        for arg in sys.argv[1:]:
            cmd += f'{arg} '
        sys.exit(os.system(cmd))