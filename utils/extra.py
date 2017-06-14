from os.path import join, abspath, dirname


def ProgressEnumerate(iterable, length=50):
    _iter = list(iterable)
    end = len(_iter)

    def _update(curr: int):
        progress = (curr + 1) / end
        bar_length = int(progress * length)

        if curr + 1 < end:
            msg = "Progress: [{0}{1}]\t {2:.3f}%{3}".format(
                '#' * bar_length,
                '-' * (length - bar_length),
                progress * 100,
                '\t'
            )
            print(msg, end='\r')
        else:
            print("Complete: [{0}]\t 100%{1}".format(length * '#', '\t' * 5))

    for i, obj in enumerate(iterable):
        _update(i)
        yield obj


def get_root_file(file=''):
    root = abspath(join(dirname(__file__), '..'))
    return join(root, file) if file else root


def get_app_data_path(file=''):
    app_data = abspath(join(dirname(__file__), '..', 'app_data'))
    return join(app_data, file) if file else app_data
