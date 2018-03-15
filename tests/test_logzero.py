#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_logzero
----------------------------------

Tests for `logzero` module.
"""

import os
import tempfile
import logging
import logzero
import pytest


# in NT os, u cant open *tempfile.NamedTemporaryFile* a second time
# which mean pass *temp* to kwarg *logfile* will raise
# a PerrmissionError.
real_NamedTemporaryFile = tempfile.NamedTemporaryFile
tempfile.NamedTemporaryFile = None

class nt_compat_cls(object):
    def __init__(self, name):
        self.name = os.path.basename(name)+'.nt_compat'

    def close(self):
        """dont know who the hell open twice on this one file?"""
        """every file name is somethig like xxxxx.nt_compat.nt_compat"""
        pass

def tearDown_nt_compat():
    tempfile.NamedTemporaryFile = None
    tempfile.NamedTemporaryFile = real_NamedTemporaryFile
    dir_files = os.listdir()
    cant_del, deled = 0, 0
    for file in dir_files:
        if file.endswith('nt_compat'):
            try:
                os.remove(file)
            except Exception as err:
                cant_del += 1
            else:
                deled += 1
    print('{} temp files for nt compatible have been delete, but {} remains.'
          .format(deled, cant_del))
    print('u may want to delete them later.')


def nt_compat(*args, **kwargs):

    def nt_compat_wrapper(*args, **kwargs):
        temp_path = real_NamedTemporaryFile(*args, **kwargs)
        nt_temp = nt_compat_cls(temp_path.name)
        temp_path.close()
        return nt_temp

    if os.name != 'nt':
        return real_NamedTemporaryFile(*args, **kwargs)
    return nt_compat_wrapper(*args, **kwargs)

tempfile.NamedTemporaryFile = nt_compat

def test_write_to_logfile_and_stderr(capsys):
    """
    Should log to a file.
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        logger = logzero.setup_logger(logfile=temp.name)
        logger.info("test log output")

        _out, err = capsys.readouterr()
        assert " test_logzero:" in err
        assert err.endswith("test log output\n")

        with open(temp.name) as f:
            content = f.read()
            assert " test_logzero:" in content
            assert content.endswith("test log output\n")
    finally:
        temp.close()

#'''
def test_custom_formatter():
    """
    Should work with a custom formatter.
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        log_format = '%(color)s[%(levelname)1.1s %(asctime)s customnametest:%(lineno)d]%(end_color)s %(message)s'
        formatter = logzero.LogFormatter(fmt=log_format)
        logger = logzero.setup_logger(logfile=temp.name, formatter=formatter)
        logger.info("test log output")

        with open(temp.name) as f:
            content = f.read()
            assert " customnametest:" in content
            assert content.endswith("test log output\n")

    finally:
        temp.close()


def test_loglevel():
    """
    Should not log any debug messages if minimum level is set to INFO
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        logger = logzero.setup_logger(logfile=temp.name, level=logging.INFO)
        logger.debug("test log output")

        with open(temp.name) as f:
            content = f.read()
            assert len(content.strip()) == 0

    finally:
        temp.close()


def test_bytes():
    """
    Should properly log bytes
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        logger = logzero.setup_logger(logfile=temp.name)

        testbytes = os.urandom(20)
        logger.debug(testbytes)
        logger.debug(None)

        # with open(temp.name) as f:
        #     content = f.read()
        #     # assert str(testbytes) in content

    finally:
        temp.close()

#'''

def test_unicode():
    """
    Should log unicode
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        logger = logzero.setup_logger(logfile=temp.name)

        msg = "😄 😁 😆 😅 😂"
        logger.debug(msg)

        with open(temp.name, "rb") as f:
            content = f.read()
            right_ans_nt_compat = {
                    ("\\xf0\\x9f\\x98\\x84 \\xf0\\x9f\\x98\\x81 \\xf0\\x9"
                     "f\\x98\\x86 \\xf0\\x9f\\x98\\x85 \\xf0\\x9f\\x98\\x8"
                     "2\\r\\n'"),
                    ("\\xf0\\x9f\\x98\\x84 \\xf0\\x9f\\x98\\x81 \\xf0\\x9"
                     "f\\x98\\x86 \\xf0\\x9f\\x98\\x85 \\xf0\\x9f\\x98\\x8"
                     "2\\n'")# notice nt use \\r\\n for a new line
             }
            assert any( right_ans in repr(content)
                        for right_ans in right_ans_nt_compat )
    finally:
        temp.close()

#'''
def test_multiple_loggers_one_logfile():
    """
    Should properly log bytes
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        logger1 = logzero.setup_logger(name="logger1", logfile=temp.name)
        logger2 = logzero.setup_logger(name="logger2", logfile=temp.name)
        logger3 = logzero.setup_logger(name="logger3", logfile=temp.name)

        logger1.info("logger1")
        logger2.info("logger2")
        logger3.info("logger3")

        with open(temp.name) as f:
            content = f.read().strip()
            assert "logger1" in content
            assert "logger2" in content
            assert "logger3" in content
            assert len(content.split("\n")) == 3

    finally:
        temp.close()


def test_default_logger(disableStdErrorLogger=False):
    """
    Default logger should work and be able to be reconfigured.
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        logzero.setup_default_logger(logfile=temp.name, disableStderrLogger=disableStdErrorLogger)
        logzero.logger.debug("debug1")  # will be logged

        # Reconfigure with loglevel ERROR
        logzero.setup_default_logger(logfile=temp.name, level=logging.ERROR, disableStderrLogger=disableStdErrorLogger)
        logzero.logger.debug("debug2")  # will not be logged
        logzero.logger.info("info1")  # will not be logged
        logzero.logger.error("error1")  # will be logged

        # Reconfigure with a different formatter
        log_format = '%(color)s[xxx]%(end_color)s %(message)s'
        formatter = logzero.LogFormatter(fmt=log_format)
        logzero.setup_default_logger(logfile=temp.name, level=logging.INFO, formatter=formatter, disableStderrLogger=disableStdErrorLogger)

        logzero.logger.info("info2")  # will be logged with new formatter
        logzero.logger.debug("debug3")  # will not be logged

        with open(temp.name) as f:
            content = f.read()
            test_default_logger_output(content)

    finally:
        temp.close()

def _check_strs_in(strs, content=None):
    must_strs = strs.get('ins')
    banned_strs = strs.get('outs')
    # check if test case is valid, a str cant not be banned while it is a must.
    assert must_strs & banned_strs == set()

    for failed in filter(lambda s:not (s in content), must_strs):
        for part in failed.split(maxsplit=2):
            assert part in content

    for failed in filter(lambda s:s in content, banned_strs):
        for part in failed.split(maxsplit=2):
            assert part in content

@pytest.mark.skip(reason="not a standalone test")
def test_default_logger_output(content):
    cases = {
            'ins':{"] debug1", "xxx] info2"},
            'outs':{"] debug2", "] info1", "] debug3"}
            }
    _check_strs_in(cases, content=content)

def test_setup_logger_reconfiguration():
    """
    Should be able to reconfigure without loosing custom handlers
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    temp2 = tempfile.NamedTemporaryFile()
    try:
        logzero.setup_default_logger(logfile=temp.name)

        # Add a custom file handler
        filehandler = logging.FileHandler(temp2.name)
        filehandler.setLevel(logging.DEBUG)
        filehandler.setFormatter(logzero.LogFormatter(color=False))
        logzero.logger.addHandler(filehandler)

        # First debug message goes to both files
        logzero.logger.debug("debug1")

        # Reconfigure logger to remove logfile
        logzero.setup_default_logger()
        logzero.logger.debug("debug2")

        # Reconfigure logger to add logfile
        logzero.setup_default_logger(logfile=temp.name)
        logzero.logger.debug("debug3")

        # Reconfigure logger to set minimum loglevel to INFO
        logzero.setup_default_logger(logfile=temp.name, level=logging.INFO)
        logzero.logger.debug("debug4")
        logzero.logger.info("info1")

        # Reconfigure logger to set minimum loglevel back to DEBUG
        logzero.setup_default_logger(logfile=temp.name, level=logging.DEBUG)
        logzero.logger.debug("debug5")

        with open(temp.name) as f:
            content = f.read()
            cases = {
                    'ins': {
                            "] debug1", "] debug3", "] info1",
                            "] debug5",
                            },
                    'outs': {
                            "] debug4", "] debug2",
                            }
                    }
            _check_strs_in(cases, content=content)

        with open(temp2.name) as f:
            content = f.read()
            cases = {
                    'ins': {
                            "] debug1", "] debug3", "] info1",
                            "] debug5", "] debug2"
                            },
                    'outs': {
                            "] debug4",
                            }
                    }
            _check_strs_in(cases, content=content)

    finally:
        temp.close()


def test_setup_logger_logfile_custom_loglevel(capsys):
    """
    setup_logger(..) with filelogger and custom loglevel
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        logger = logzero.setup_logger(logfile=temp.name, fileLoglevel=logging.WARN)
        logger.info("info1")
        logger.warn("warn1")

        with open(temp.name) as f:
            content = f.read()
            assert "] info1" not in content
            assert "] warn1" in content

    finally:
        temp.close()


def test_log_function_call():
    @logzero.log_function_call
    def example():
        """example doc"""
        pass

    assert example.__name__ == "example"
    assert example.__doc__ == "example doc"


def test_default_logger_logfile_only(capsys):
    """
    Run the ``test_default_logger`` with ``disableStdErrorLogger`` set to ``True`` and
    confirm that no data is written to stderr
    """
    test_default_logger(disableStdErrorLogger=True)
    out, err = capsys.readouterr()
    assert err == ''


def test_default_logger_stderr_output(capsys):
    """
    Run the ``test_default_logger`` and confirm that the proper data is written to stderr
    """
    test_default_logger()
    out, err = capsys.readouterr()
    test_default_logger_output(err)


def test_default_logger_syslog_only(capsys):
    """
    Run a test logging to ``syslog`` and confirm that no data is written to stderr.
    Note that the output in syslog is not currently being captured or checked.
    """
    logzero.reset_default_logger()
    logzero.syslog()
    logzero.logger.error('debug')
    out, err = capsys.readouterr()
    assert out == '' and err == ''
#'''
if __name__ == '__main__':
    pytest.main([__file__, '-x'])
    tearDown_nt_compat()
else:
    tearDown_nt_compat()

