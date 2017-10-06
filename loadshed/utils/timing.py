import timeit
import datetime

start_time = 0
lap_time = 0  # level 1
lap_time2 = 0  # level 2


def start():
    """
    Start timing
    :return: nothing
    """
    global start_time
    global lap_time
    global lap_time2
    start_time = lap_time = lap_time2 = timeit.default_timer()
    time_now = datetime.datetime.now()
    print(f'Started at {time_now.strftime("%I:%M%p")}')


def lap(is_print_out=False):
    """
    Calc the elapsed time from the previous lap (i.e. lap_time).

    :return: int
    """
    global lap_time
    current_time = timeit.default_timer()
    s_out = time2str(current_time - lap_time)
    lap_time = current_time
    if is_print_out: print(s_out)
    return s_out


def lap2(is_print_out=False):
    """
    Calc the elapsed time from the previous lap (i.e. lap_time).

    :return: int
    """
    global lap_time2
    current_time = timeit.default_timer()
    s_out = time2str(current_time - lap_time2)
    lap_time2 = current_time
    if is_print_out: print(s_out)
    return s_out


def stop(is_print_out=True):
    """
    Print out the elapsed time from the start time (i.e. start_time).

    :return: nothing
    """
    global start_time
    current_time = timeit.default_timer()
    time_now = datetime.datetime.now()
    s_out = 'Stopped at {}, total: {}'.format(time_now.strftime('%I:%M%p '), time2str(current_time - start_time))
    if is_print_out: print(s_out)
    return s_out


def stop_full(is_print_out=False):
    """
    Print out the elapsed time from the start time (i.e. start_time).

    :return: nothing
    """
    global start_time
    current_time = timeit.default_timer()
    time_now = datetime.datetime.now()
    s_out = 'Stopped at {} in {}'.format(time_now.strftime('%I:%M%p %d/%m/%Y'), time2str(current_time - start_time))
    if is_print_out: print(s_out)
    return s_out


def stop_inline():
    """
    Print out the elapsed time from the start time (i.e. start_time).

    :return: nothing
    """
    global start_time
    current_time = timeit.default_timer()
    s_out = '[{}]'.format(time2str(current_time - start_time))
    print(s_out)


def time2str(seconds):
    """
    Convert number of elapsed time (in seconds, a float number) to a string.

    :param seconds: e.g. 62.15
    :return: e.g. 1m 2.15s
    """
    if seconds < 60:
        s_out = '{:.2f}s'.format(seconds)
    else:
        mins = int(seconds / 60)
        seconds -= 60 * mins  # float
        s_out = '{}m {:.2f}s'.format(mins, seconds)
    return s_out
