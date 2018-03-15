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
import pytest
import logzero


def _check_strs_in(strs, content=None):
    must_strs = strs.get('ins')
    banned_strs = strs.get('outs')
    # check if test case is valid, a str cant not be banned while it is a must.
    assert must_strs & banned_strs == set()

    for failed in filter(lambda s: not (s in content), must_strs):
        for part in failed.split(maxsplit=2):
            assert part in content

    for failed in filter(lambda s: s in content, banned_strs):
        for part in failed.split(maxsplit=2):
            assert part in content


def test_api_logfile(capsys):
    """
    logzero.logfile(..) should work as expected
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        logzero.logger.info("info1")

        # Set logfile
        logzero.logfile(temp.name)
        logzero.logger.info("info2")

        # Remove logfile
        logzero.logfile(None)
        logzero.logger.info("info3")

        # Set logfile again
        logzero.logfile(temp.name)
        logzero.logger.info("info4")

        with open(temp.name) as f:
            content = f.read()
            cases = {
                'ins': {
                    "] info2", "] info4"
                },
                'outs': {
                    "] info1", "] info3"
                }
            }
            _check_strs_in(cases, content=content)

    finally:
        temp.close()


def test_api_loglevel(capsys):
    """
    Should reconfigure the internal logger loglevel
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        logzero.logfile(temp.name)
        logzero.logger.info("info1")
        logzero.loglevel(logging.WARNING)
        logzero.logger.info("info2")
        logzero.logger.warning("warning1")

        with open(temp.name) as f:
            content = f.read()
            cases = {
                'ins': {
                    "] info1", "] warning1"
                },
                'outs': {
                    "] info2"
                }
            }
            _check_strs_in(cases, content=content)

    finally:
        temp.close()


def test_api_loglevel_custom_handlers(capsys):
    """
    Should reconfigure the internal logger loglevel and custom handlers
    """
    logzero.reset_default_logger()
    # TODO
    pass
    # temp = tempfile.NamedTemporaryFile()
    # try:
    #     logzero.logfile(temp.name)
    #     logzero.logger.info("info1")
    #     logzero.loglevel(logging.WARNING)
    #     logzero.logger.info("info2")
    #     logzero.logger.warning("warning1")

    #     with open(temp.name) as f:
    #         content = f.read()
    #         assert "] info1" in content
    #         assert "] info2" not in content
    #         assert "] warning1" in content

    # finally:
    #     temp.close()


def test_api_rotating_logfile(capsys):
    """
    logzero.rotating_logfile(..) should work as expected
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        logzero.logger.info("info1")

        # Set logfile
        logzero.logfile(temp.name, maxBytes=10, backupCount=3)
        logzero.logger.info("info2")
        logzero.logger.info("info3")

        with open(temp.name) as f:
            content = f.read()
            cases = {
                'ins': {
                    "] info3"
                },
                'outs': {
                    "] info1", "] info2"
                }
            }
            _check_strs_in(cases, content=content)

        fn_rotated = temp.name + ".1"
        assert os.path.exists(fn_rotated)
        with open(fn_rotated) as f:
            content = f.read()
            assert "] info2" in content

    finally:
        temp.close()


def test_api_logfile_custom_loglevel():
    """
    logzero.logfile(..) should be able to use a custom loglevel
    """
    logzero.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        # Set logfile with custom loglevel
        logzero.logfile(temp.name, loglevel=logging.WARNING)
        logzero.logger.info("info1")
        logzero.logger.warning("warning1")

        # If setting a loglevel with logzero.loglevel(..) it will not overwrite
        # the custom loglevel of the file handler
        logzero.loglevel(logging.INFO)
        logzero.logger.info("info2")
        logzero.logger.warning("warning2")

        with open(temp.name) as f:
            content = f.read()
            cases = {
                'ins': {
                    "] warning2", "] warning1"
                },
                'outs': {
                    "] info2", "] info1"
                }
            }
            _check_strs_in(cases, content=content)

    finally:
        temp.close()


if __name__ == '__main__':
    pytest.main(['-q', __file__])
