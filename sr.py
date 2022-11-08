#!/usr/bin/python3
import os
from colorama import Fore

# get connected screens
def connected_screens():
    # Filter and parse all screens connected
    screens = {
        screen.split(' connected ')[0]: {
            'resolution': screen.split(' connected ')[1].split('+')[0],
            'offset x' : screen.split(' connected ')[1].split('+')[1],
            'offset y' : screen.split(' connected ')[1].split('+')[2].split(' ')[0],
        }
        for screen in os.popen('xrandr -q').read().split('\n')
        if ' connected ' in screen
    }
    
    return screens

def audio_cards():
    # Filter and parse all audio cards
    cards = {
        card.split(': ')[0]: {
            'id': card.split(': ')[0].split('card ')[1],
            'info': card.split(': ')[1],
        }
        for card in os.popen('arecord -l').read().split('\n')
        if 'card ' in card
    }
    return cards

# record screen
def record_screen(screen, output_path, record_mic=False, default_mic=False, audio_card=None):
    # Use ffpmeg
    command =  f'ffmpeg'
    
    # Select where to get the video from
    command += f' -f x11grab'
    
    # Select screen resolution
    command += f' -s {screen["resolution"]}'
    
    # Select screen offset (what screen you are using if you have multiple screens)
    command += f' -i :0.00+{screen["offset x"]},{screen["offset y"]}'

    if record_mic:
        # Select where to get audio from
        command += f' -f alsa'
        if default_mic:
            # Select audio channels
            command += f' -ac 2'
            # Select what alsa device to use
            command += f' -i default'
        else:
            if not audio_card:
                print('Failed, to record, No audio card')
                exit(1)

                # NOTE: For some reason, this doesn't work for me,
                # so atm, I see this as broken, so just use the default device for now
            
                # Select audio channels
                command += f' -ac 2'
                # Select alsa device to use
                command += f' -i hw:{audio_card["id"]}'

    # Where to save the video
    command += f' {output_path}'

    print(f'{Fore.YELLOW}COMMAND: {Fore.GREEN}{command}{Fore.WHITE}')

    print(f'\n{Fore.YELLOW}NOTE:{Fore.WHITE}',
          'To stop the recording,',
          'press CTRL C while having the terminal selected,',
          'or just pres Q')
    
    msg  = f'\n{Fore.YELLOW}is this the correct ffmpeg command?'
    msg += f'\n{Fore.CYAN}--({Fore.GREEN}y{Fore.WHITE}/{Fore.RED}n{Fore.CYAN})-> {Fore.WHITE}'
    ans=input(msg)
    if ans.lower() != 'y': return

    os.system(command)
    
screens = connected_screens()
screen = screens['eDP']

cards = audio_cards()
card = cards['card 1']

#print(screen)
#print(card)

record_screen(screen, 'test.mkv',  record_mic=True, default_mic=True)
