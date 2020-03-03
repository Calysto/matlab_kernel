import sys
from metakernel import __version__ as mversion
from . import __version__
from .kernel import MatlabKernel


if __name__ == "__main__":
    print('Matlab kernel v%s' % __version__)
    print('Metakernel v%s' % mversion)
    print('Python v%s' % sys.version)
    print('Python path: %s' % sys.executable)
    print('\nConnecting to Matlab...')
    try:
        m = MatlabKernel()
        print('Matlab connection established')
        print(m.banner)
        print(m.do_execute_direct('disp("hi from Matlab!")'))
    except Exception as e:
        print(e)
