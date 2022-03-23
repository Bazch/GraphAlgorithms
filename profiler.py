import cProfile, pstats, io


def profiler(fnc):
    """A decorator that uses cProfile to profile a function"""

    def inner(args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sort_by = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner
