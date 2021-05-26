"""
Generic linux daemon base class for python 3.x.
"""


class Angel():
    """
    A generic non-daemon process class.
    Usage: subclass Angel and override the run() method.

    Written to swap out for Daemon used by Looper due to background threads being unable to log to LogDNA
    """

    def __init__(self, pidfile):
        self.pidfile = pidfile

    def start(self):
        """
        Start the timeloop.
        """
        self.run()

    def stop(self):
        """
        Stop the timeloop.
        """
        self.end()

    def restart(self):
        """
        Restart the non-daemon process.
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Angel.
        It will be called by start() or indirectly by restart().
        """

    def end(self):
        """
        You should override this method when you subclass Angel.
        It will be called by stop() or indirectly by restart().
        """
