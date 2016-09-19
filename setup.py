import sys

from setuptools import setup, find_packages
import versioneer


if __name__ == "__main__":
    if sys.version_info.major < 3:
        raise ImportError("matlab_kernel requires Python>=3.3")

    setup(name="matlab_kernel",
          author="Steven Silvester, Antony Lee",
          version=versioneer.get_version(),
          cmdclass=versioneer.get_cmdclass(),
          url="https://github.com/Calysto/matlab_kernel",
          license="BSD",
          long_description=open("README.rst").read(),
          classifiers=["Framework :: IPython",
                       "License :: OSI Approved :: BSD License",
                       "Programming Language :: Python :: 3.5",
                       "Topic :: System :: Shells",],
          packages=find_packages(include=["matlab_kernel", "matlab_kernel.*"]),
          install_requires=["metakernel>=0.13.1"],
          )
