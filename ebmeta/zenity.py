"""Functions for accessing Zenity GUI scripting tool."""

from ebmeta import shell

class ZenityCancelled(Exception):
    pass

def edit_string(text, prompt=None):
    args = [
        'zenity',
        '--width=700',
        '--height=550',
        '--text-info',
        '--editable'
    ]
    if prompt: args.extend(['--title', prompt])
    (text, exitcode) = shell.pipe_with_exitcode(args, text)
    if exitcode: raise ZenityCancelled
    return text

if __name__ == '__main__':
    try:
        text = edit_string('text', 'prompt')
        print('Result:')
        print(text)
    except ZenityCancelled:
        print('Cancelled.')
