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
            script.write(f'#!/bin/sh\n{controller} $@ | aria2c -c -d "{dl_dir}" -i -')
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
    print(f'''For the first time, you should run:
    {sys.argv[0]} init

After making sure everything's ready, you can run:
    {sys.argv[0]} <song_id> [<song_id2> <song_id3> ...]
    ''')
    sys.exit(1)

if __name__ == '__main__':

    if 'init' in sys.argv:
        init()

    elif len(sys.argv) >= 2 and os.path.isdir(install_path):

        args = ''
        for id in sys.argv[1:]:
            if id.isdigit():
                args += f'{id} '
            else:
                print(f'Invalid argument: {id}\n')
                how_to_use()

        exit_code=os.system(f'{install_path}/gdcsd.{script_type} {args}')
        if exit_code:
            sys.exit()

        for id in sys.argv[1:]:
            target = f'{dl_dir}/{id}.mp3'
            try:
                with open(target) as f:
                    f.read()
                os.remove(target)
                print(f'Song ID {id} doesn\'t seem to have a direct link.')
                print(f'Try visiting https://newgrownds.com/audio/listen/{id} to download it manually.')
            except UnicodeDecodeError:
                pass

    else:
        how_to_use()

