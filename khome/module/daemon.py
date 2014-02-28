import os
import sys

def possess_me():
    """
    Sign a contract with Oblivion's leader to get new power. This amount of
    power transforms you into a d(a)emon. You are now invincible and can only
    be killed by a super sayan (or not). But be careful with this new power.
    One day, a wise man said "With great power comes great responsibility". You
    can use those skills as you like. Either as a tyrannic and oppressive
    d(a)emon or you can repent yourself at the side of the super sayan to fight
    crime.
    """

    # fork the first time (to make a non-session-leader child process)
    try:
        pid = os.fork()
    except OSError, e:
        raise RuntimeError('1st fork failed: %s [%d]' % (e.strerror, e.errno))
    if pid != 0:
        os._exit(0)

    # detach from controlling terminal (to make child a session-leader)
    os.setsid()
    try:
        pid = os.fork()
    except OSError, e:
        raise RuntimeError('2nd fork failed: %s [%d]' % (e.strerror, e.errno))
    if pid != 0:
        # child process is all done
        os._exit(0)

    # grandchild process now non-session-leader, detached from parent
    # grandchild process must now close all open files
    try:
        maxfd = os.sysconf("SC_OPEN_MAX")
    except (AttributeError, ValueError):
        maxfd = 1024

    for fd in range(maxfd):
        try:
           os.close(fd)
        except OSError: # ERROR, fd wasn't open to begin with (ignored)
           pass

    # redirect stdin, stdout and stderr to /dev/null
    os.open(os.devnull, os.O_RDWR)  # standard input (0)
    os.dup2(0, 1)
    os.dup2(0, 2)

    return 0
