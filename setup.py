import glob
from setuptools import setup, find_packages

with open('matlab_kernel/__init__.py', 'rb') as fid:
    for line in fid:
        line = line.decode('utf-8')
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break

DISTNAME = 'matlab_kernel'
PACKAGE_DATA = {
    DISTNAME: ['*.m'] + glob.glob('%s/**/*.*' % DISTNAME)
}
DATA_FILES = [
    ('share/jupyter/kernels/matlab', [
        '%s/kernel.json' % DISTNAME
     ] + glob.glob('%s/images/*.png' % DISTNAME)
    )
]

if __name__ == "__main__":
    setup(name="matlab_kernel",
          author="Steven Silvester, Antony Lee",
          version=version,
          url="https://github.com/Calysto/matlab_kernel",
          license="BSD",
          long_description=open("README.rst").read(),
          long_description_content_type='text/x-rst',
          classifiers=["Framework :: IPython",
                       "License :: OSI Approved :: BSD License",
                       "Programming Language :: Python :: 3.4",
                       "Programming Language :: Python :: 3.5",
                       "Topic :: System :: Shells"],
          packages=find_packages(include=["matlab_kernel", "matlab_kernel.*"]),
          package_data=PACKAGE_DATA,
          include_package_data=True,
          data_files=DATA_FILES,
          requires=["metakernel (>0.23.0)", "jupyter_client (>=4.4.0)",
                    "ipython (>=4.0.0)"],
          install_requires=["metakernel>=0.23.0", "jupyter_client >=4.4.0",
                            "ipython>=4.0.0",
                            "backports.tempfile;python_version<'3.0'",
                            'wurlitzer>=1.0.2;platform_system!="Windows"']
          )
