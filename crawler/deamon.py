#!/usr/bin/env python

import sys
import os
import time
import atexit
from signal import SIGTERM
import datetime


class Daemon:
    """
    A generic daemon class.
    Usage: subclass the Daemon class and override the run() method

    Copycat from: http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
    """
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
        Do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)  # The first worker
                os.kill(pid+1, SIGTERM)  # The second worker
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                else:
                    print str(err)
                    sys.exit(1)

        # os.system('pkill gunicorn')
        os.system("ps aux | grep '/home/agurkas/crawler/' | awk '{print $2}' | xargs -r kill -9")
        # Filtering out process, which runs in `cra_targetprice` directory and kill it

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be
        called after the process has been
        daemonized by start() or restart().
        """


class cra_daemon(Daemon):
    def run(self):
        # Crawler binds on 9050 port
        os.system('cd /home/agurkas/crawler/releases/current/crawler;\
            python2 crawler.py')

if __name__ == '__main__':
    """
    This is the main worker here
    """
    log_date = datetime.datetime.now().strftime('%Y-%m-%d')
    log_path = "/var/log/cra_everything_" + log_date + ".log"
    deamon = cra_daemon('/tmp/cra-deamon.pid', '/dev/null', log_path, log_path)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print "Starting server... "
            deamon.start()
        elif 'stop' == sys.argv[1]:
            print "Stopping server... "
            deamon.stop()
        elif 'restart' == sys.argv[1]:
            print "Restarting server... "
            deamon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "Usage %s start|stop|restart" % sys.argv[0]
