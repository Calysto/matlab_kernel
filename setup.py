from distutils.command.install import install
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

class install_with_kernelspec(install):
    def run(self):
        install.run(self)
        from IPython.kernel.kernelspec import install_kernel_spec
        from IPython.utils.tempdir import TemporaryDirectory
        from metakernel.utils.kernel import install_kernel_resources
        with TemporaryDirectory() as td:
            os.chmod(td, 0o755) # Starts off as 700, not user readable
            with open(os.path.join(td, 'kernel.json'), 'w') as f:
                json.dump(kernel_json, f, sort_keys=True)
            log.info('Installing kernel spec')
            try:
                install_kernel_spec(td, 'matlab_kernel', user=self.user,
                                    replace=True)
            except:
                install_kernel_spec(td, 'matlab_kernel', user=not self.user,
                                    replace=True)

svem_flag = '--single-version-externally-managed'
if svem_flag in sys.argv:
    # Die, setuptools, die.
    sys.argv.remove(svem_flag)

setup(name='matlab_kernel',
      version='0.1.0',
      description='A Matlab kernel for Jupyter/IPython',
      long_description="A Matlab kernel for Jupyter/IPython, based on MetaKernel",
      url="https://github.com/calysto/matlab_kernel/tree/master/matlab_kernel",
      author='Steven Silvester',
      author_email='steven.silvester@ieee.org',
      py_modules=['matlab_kernel'],
      requires=["metakernel (>=0.8)", "pymatbridge", "IPython (>=3.0)"],
      cmdclass={'install': install_with_kernelspec},
      classifiers = [
          'Framework :: IPython',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 2',
          'Topic :: System :: Shells',
      ]
)
