from distutils.core import setup
from distutils import log
import os
import json
import sys

kernel_json = {
    "argv": [sys.executable,
	     "-m", "matlab_kernel",
	     "-f", "{connection_file}"],
    "display_name": "Matlab",
    "language": "matlab",
    "name": "matlab_kernel",
}


def install_spec():
    user = '--user' in sys.argv
    from IPython.kernel.kernelspec import install_kernel_spec
    from IPython.utils.tempdir import TemporaryDirectory
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)  # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
        log.info('Installing kernel spec')
        try:
            install_kernel_spec(td, "matlab_kernel", user=user,
                                replace=True)
        except:
            install_kernel_spec(td, "matlab_kernel", user=not user,
                                replace=True)

if 'install' in sys.argv or 'develop' in sys.argv:
    install_spec()


svem_flag = '--single-version-externally-managed'
if svem_flag in sys.argv:
    # Die, setuptools, die.
    sys.argv.remove(svem_flag)


with open('matlab_kernel.py') as fid:
    for line in fid:
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break

setup(name='matlab_kernel',
      version=version,
      description='A Matlab kernel for Jupyter/IPython',
      long_description= open('README.rst', 'r').read(),
      url="https://github.com/calysto/matlab_kernel",
      author='Steven Silvester',
      author_email='steven.silvester@ieee.org',
      py_modules=['matlab_kernel'],
      license="MIT",
      requires=["metakernel (>=0.8)", "pymatbridge", "IPython (>=3.0)"],
      classifiers = [
          'Framework :: IPython',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 2',
          'Topic :: System :: Shells',
      ]
)
