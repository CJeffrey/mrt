import os


class TestLogging(object):
    def test_init_logging(self):
        """
        Test logging function
        """
        # TODO: test a tmp log file
        log_file = 'mrt.log'
        assert os.path.isfile(log_file)
