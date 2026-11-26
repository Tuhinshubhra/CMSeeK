#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information

# Regression tests for the site list (-l/--list) path handling.
# Run with: python3 -m unittest discover -s tests -v

import os
import subprocess
import sys
import tempfile
import unittest

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CMSEEK_PY = os.path.join(REPO_DIR, 'cmseek.py')
INVALID_PATH_MESSAGE = 'Invalid path! CMSeeK is quitting'


def run_cmseek(*args):
    # stdin is fed with a few newlines because cmseek asks for an [ENTER] when
    # the result index could not be created on a fresh checkout
    return subprocess.run(
        [sys.executable, CMSEEK_PY] + list(args),
        cwd=REPO_DIR,
        input=b'\n\n\n',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180)


class InvalidListPathTest(unittest.TestCase):
    '''
    A path that cannot be read as a list of URLs has to be reported the same
    way as a missing file: one line error message, no traceback, non zero exit
    code.
    '''

    def assert_clean_path_error(self, path):
        proc = run_cmseek('-l', path)
        stdout = proc.stdout.decode('utf-8', 'replace')
        stderr = proc.stderr.decode('utf-8', 'replace')
        self.assertNotIn('Traceback', stderr,
                         'unhandled exception for -l ' + path + '\n' + stderr)
        self.assertIn(INVALID_PATH_MESSAGE, stdout,
                      'missing error message for -l ' + path)
        self.assertNotEqual(0, proc.returncode,
                            'CMSeeK exited successfully for -l ' + path)

    def test_missing_file(self):
        self.assert_clean_path_error(
            os.path.join(tempfile.gettempdir(), 'cmseek-no-such-list.txt'))

    def test_directory(self):
        self.assert_clean_path_error(tempfile.gettempdir())

    def test_file_is_not_utf8(self):
        handle, path = tempfile.mkstemp(suffix='.bin')
        try:
            with os.fdopen(handle, 'wb') as blob:
                blob.write(b'\xff\xfe\x00\x00 not a url list \x81\n')
            self.assert_clean_path_error(path)
        finally:
            os.remove(path)

    @unittest.skipIf(hasattr(os, 'geteuid') and os.geteuid() == 0,
                     'running as root, file modes are not enforced')
    def test_file_is_not_readable(self):
        handle, path = tempfile.mkstemp(suffix='.txt')
        try:
            with os.fdopen(handle, 'w') as urls:
                urls.write('http://example.com\n')
            os.chmod(path, 0)
            self.assert_clean_path_error(path)
        finally:
            os.chmod(path, 0o600)
            os.remove(path)


if __name__ == '__main__':
    unittest.main()
