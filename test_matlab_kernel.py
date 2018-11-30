"""Example use of jupyter_kernel_test, with tests for IPython."""

import unittest
from jupyter_kernel_test import KernelTests


class MatlabKernelTests(KernelTests):
    kernel_name = "matlab"
    language_name = "matlab"
    code_hello_world = "disp('hello, world')"
    completion_samples = [
        {'text': 'one',
         'matches': {'ones'}},
    ]
    code_page_something = "ones?"


if __name__ == '__main__':
    unittest.main()
