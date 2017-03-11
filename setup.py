from setuptools import setup, find_packages

with open('matlab_kernel/__init__.py', 'rb') as fid:
    for line in fid:
        line = line.decode('utf-8')
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break


if __name__ == "__main__":
    setup(name="matlab_kernel",
          author="Steven Silvester, Antony Lee",
          version=version,
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
                            "backports.tempfile;python_version<'3.0'"]
          )
