import json
import os
import sys

try:
    from jupyter_client.kernelspec import install_kernel_spec
except ImportError:
    from IPython.kernel.kernelspec import install_kernel_spec
from IPython.utils.tempdir import TemporaryDirectory


kernel_json = {
    "argv": [sys.executable,
             "-m", "matlab_kernel",
             "-f", "{connection_file}"],
    "display_name": "Matlab",
    "language": "matlab",
    "mimetype": "text/x-octave",
    "name": "matlab",
}


def install_my_kernel_spec(user=True):
    user = '--user' in sys.argv or not _is_root()
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)  # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
        kernel_name = kernel_json['name']
        try:
            install_kernel_spec(td, kernel_name, user=user,
                                replace=True)
        except:
            install_kernel_spec(td, kernel_name, user=not user,
                                replace=True)


def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False  # assume not an admin on non-Unix platforms


def main(argv=[]):
    user = '--user' in argv or not _is_root()
    install_my_kernel_spec(user=user)


if __name__ == '__main__':
    main(argv=sys.argv)
