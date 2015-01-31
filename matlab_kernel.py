from __future__ import print_function

from metakernel import MetaKernel
from pymatbridge import Matlab
from IPython.display import Image


class MatlabKernel(MetaKernel):
    implementation = 'Matlab Kernel'
    implementation_version = '1.0'
    language = 'matlab'
    language_version = '0.1'
    banner = "Matlab Kernel"
    language_info = {
        'mimetype': 'text/x-matlab',
        'name': 'bash',
        # ------ If different from 'language':
        # 'codemirror_mode': {
        #    "version": 2,
        #    "name": "ipython"
        # }
        # 'pygments_lexer': 'language',
        # 'version'       : "x.y.z",
        'file_extension': '.m',
        'help_links': MetaKernel.help_links,
    }

    def __init__(self, *args, **kwargs):
        excecutable = kwargs.pop('excecutable', 'matlab')
        super(MatlabKernel, self).__init__(*args, **kwargs)
        self._matlab = Matlab(excecutable)
        self._matlab.start()

    def get_usage(self):
        return "This is the Matlab kernel."

    def do_execute_direct(self, code):
        code = code.strip()
        if not code:
            return
        self.log.debug('execute: %s' % code)
        resp = self._matlab.run_code(code.strip())
        self.log.debug('execute done')
        if 'stdout' not in resp['content']:
            raise ValueError(resp)
        if 'figures' in resp['content']:
            for fname in resp['content']['figures']:
                im = Image(filename=fname)
                self.Display(im)
        return resp['content']['stdout'].strip()

    def get_kernel_help_on(self, info, level=0, none_on_fail=False):
        code = info['code'].strip()
        if not code or len(code.split()) > 1:
            if none_on_fail:
                return None
            else:
                return ""
        resp = self._matlab.run_code('help %s' % code)
        return resp['content'].get('stdout', '')

    def repr(self, data):
        return data

if __name__ == '__main__':
    from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=MatlabKernel)
