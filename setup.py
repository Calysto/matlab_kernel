
from setuptools import setup, find_packages
import versioneer


if __name__ == "__main__":
    setup(name="matlab_kernel",
          author="Steven Silvester, Antony Lee",
          version=versioneer.get_version(),
          cmdclass=versioneer.get_cmdclass(),
          url="https://github.com/Calysto/matlab_kernel",
          license="BSD",
          long_description=open("README.rst").read(),
          classifiers=["Framework :: IPython",
                       "License :: OSI Approved :: BSD License",
                       "Programming Language :: Python :: 3.4",
                       "Programming Language :: Python :: 3.5",
                       "Topic :: System :: Shells"],
          packages=find_packages(include=["matlab_kernel", "matlab_kernel.*"]),
          requires=["metakernel (>0.18.0)", "jupyter_client (>=4.4.0)",
                    "pathlib", 'ipython (>=4.0.0)'],
          install_requires=["metakernel>=0.18.0", "jupyter_client >=4.4.0",
                            "ipython>=4.0.0",
                            "pathlib;python_version<'3.4'",
                            "backports.tempfile;python_version<'3.0'"]
          )
