import webbrowser

from worldgen.generate import main_loop, _F_SIZE


if __name__ == '__main__':
    # prompt = input('What world do you want to play in? ')
    prompt = 'Equirectangular render of a psychedelic alien world, from a first-person point of view, 8k uhd'
    settings = {'n': 1, 'size': f'{_F_SIZE}x{_F_SIZE}', 'prompt': prompt}
    # main_loop(settings)

    url = 'file:///path/to/your/file/testdata.html'
    webbrowser.open(url, new=2)  # open in new tab