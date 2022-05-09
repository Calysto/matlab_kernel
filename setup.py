import glob
import json
import os
import sys
from setuptools import setup, find_packages

with open('matlab_kernel/__init__.py', 'rb') as fid:
    for line in fid:
        line = line.decode('utf-8')
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break

DISTNAME = 'matlab_kernel'
PY_EXECUTABLE = 'python'

# when building wheels, directly use 'python' in the kernelspec.
if any(a.startswith("bdist") for a in sys.argv):
    PY_EXECUTABLE = 'python'

# when directly installing, use sys.executable to get python full path.
if any(a.startswith("install") for a in sys.argv):
    PY_EXECUTABLE = sys.executable

# generating kernel.json for both kernels
os.makedirs(os.path.join(DISTNAME, 'matlab'), exist_ok=True)
with open(os.path.join(DISTNAME, 'kernel_template.json'), 'r') as fp:
    matlab_json = json.load(fp)
matlab_json['argv'][0] = PY_EXECUTABLE
with open(os.path.join(DISTNAME, 'matlab','kernel.json'), 'w') as fp:
    json.dump(matlab_json, fp)

os.makedirs(os.path.join(DISTNAME, 'matlab_connect'), exist_ok=True)
with open(os.path.join(DISTNAME, 'kernel_template.json'), 'r') as fp:
    matlab_json = json.load(fp)
matlab_json['argv'][0] = PY_EXECUTABLE
matlab_json['display_name'] = 'Matlab (Connection)'
matlab_json['name'] = "matlab_connect"
matlab_json['env'] = {'connect-to-existing-kernel': '1'}
with open(os.path.join(DISTNAME, 'matlab_connect','kernel.json'), 'w') as fp:
    json.dump(matlab_json, fp)

PACKAGE_DATA = {
    DISTNAME: ['*.m'] + glob.glob('%s/**/*.*' % DISTNAME)
}
DATA_FILES = [
    ('share/jupyter/kernels/matlab', [
        '%s/matlab/kernel.json' % DISTNAME
     ] + glob.glob('%s/images/*.png' % DISTNAME)
    ), 
    ('share/jupyter/kernels/matlab_connect', [
        '%s/matlab_connect/kernel.json' % DISTNAME
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
