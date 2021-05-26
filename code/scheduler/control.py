import sys

from utils.logging.configure import get_logger

from scheduler.looper import Looper



# Configure and create our logger
logger = get_logger()


def main():
    process = Looper('/tmp/looper.pid')

    logger.info('**********************************')
    if len(sys.argv) == 2:
        if sys.argv[1] == 'start':
            logger.info('starting process')
            process.start()
        elif sys.argv[1] == 'stop':
            logger.info('stopping process')
            process.stop()
        elif sys.argv[1] == 'restart':
            logger.info('restarting process')
            process.restart()
        else:
            logger.info('Unknown command')
            sys.exit(2)
        sys.exit(0)
    else:
        logger.info('Usage: %s start|stop|restart', sys.argv[0])
        sys.exit(2)


if __name__ == "__main__":
    # pylint: disable=pointless-string-statement
    '''
    cd code
    PYTHONPATH=$PYTHONPATH:$(pwd) python code/control.py start|stop|restart
    '''
    main()
