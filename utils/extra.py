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
