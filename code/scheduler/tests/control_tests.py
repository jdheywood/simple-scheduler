from unittest.mock import call, patch

import unittest

from scheduler.control import main


class SchedulerControlTestCase(unittest.TestCase):
    def setUp(self):  # sourcery skip: extract-duplicate-method
        logger_patch = patch('scheduler.control.logger')
        self.logger = logger_patch.start()
        self.addCleanup(logger_patch.stop)

        looper_patch = patch('scheduler.control.Looper')
        self.looper = looper_patch.start()
        self.addCleanup(looper_patch.stop)

        sys_patch = patch('scheduler.control.sys')
        self.sys = sys_patch.start()
        self.addCleanup(sys_patch.stop)

    def test_starts_daemon_when_correct_parameters_supplied(self):
        testargs = ['scheduler/control.py', 'start']
        self.sys.argv = testargs

        main()

        self.looper.assert_called_once_with('/tmp/looper.pid')

        self.logger.info.assert_has_calls([
            call('**********************************'),
            call('starting process'),
        ])

        self.sys.exit.assert_called_once_with(0)

    def test_stops_daemon_when_correct_parameters_supplied(self):
        testargs = ['scheduler/control.py', 'stop']
        self.sys.argv = testargs

        main()

        self.looper.assert_called_once_with('/tmp/looper.pid')

        self.logger.info.assert_has_calls([
            call('**********************************'),
            call('stopping process'),
        ])

        self.sys.exit.assert_called_once_with(0)

    def test_restarts_daemon_when_correct_parameters_supplied(self):
        testargs = ['scheduler/control.py', 'restart']
        self.sys.argv = testargs

        main()

        self.looper.assert_called_once_with('/tmp/looper.pid')

        self.logger.info.assert_has_calls([
            call('**********************************'),
            call('restarting process'),
        ])

        self.sys.exit.assert_called_once_with(0)

    def test_logs_usage_message_when_no_control_parameter_supplied(self):
        testargs = ['scheduler/control.py']
        self.sys.argv = testargs

        main()

        self.looper.assert_called_once_with('/tmp/looper.pid')

        self.logger.info.assert_has_calls([
            call('**********************************'),
            call('Usage: %s start|stop|restart', testargs[0]),
        ])

        self.sys.exit.assert_called_once_with(2)

    def test_logs_unknown_command_message_when_incorrect_parameters_supplied(self):
        testargs = ['scheduler/control.py', 'kwyjibo']
        self.sys.argv = testargs

        main()

        self.looper.assert_called_once_with('/tmp/looper.pid')

        self.logger.info.assert_has_calls([
            call('**********************************'),
            call('Unknown command'),
        ])

        self.sys.exit.assert_has_calls([
            call(2),
            call(0),
        ])
