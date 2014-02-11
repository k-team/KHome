import time
import os
import sys
sys.path.append('./core')
import daemon
from module import get_pid_file

if __name__ == '__main__':
    try:
        module_name = sys.argv[1]
    except IndexError:
        sys.exit(1)

    daemon.possess_me()
    # Trololol i'm a demon

    pid_file = get_pid_file(module_name)
    if os.path.exists(pid_file):
        raise RuntimeError('A pid file already exist for this module')
        sys.exit(1)
    else:
        try:
            with open(get_pid_file(module_name), 'w') as f:
                f.write(str(os.getpid()))
                f.flush()
        except (OSError, IOError), e:
            os.remove(pid_file)
            sys.exit(0)
        else:
            print 'I\'m the super demon'
            time.sleep(10)
            os.remove(pid_file)
            sys.exit(0)
