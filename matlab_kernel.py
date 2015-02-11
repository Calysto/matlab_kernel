from __future__ import print_function

from metakernel import MetaKernel
from pymatbridge import Matlab
from IPython.display import Image


__version__ = '0.3'


class MatlabKernel(MetaKernel):
    implementation = 'Matlab Kernel'
    implementation_version = __version__,
    language = 'matlab'
    language_version = '0.1',
    banner = "Matlab Kernel"
    language_info = {
        'mimetype': 'text/x-matlab',
        'name': 'matlab',
        'file_extension': '.m',
        'help_links': MetaKernel.help_links,
    }

    _first = True

    def __init__(self, *args, **kwargs):
        excecutable = kwargs.pop('excecutable', 'matlab')
        super(MatlabKernel, self).__init__(*args, **kwargs)
        self._matlab = Matlab(excecutable)
        self._matlab.start()

    def get_usage(self):
        return "This is the Matlab kernel."

    def do_execute_direct(self, code):
        if self._first:
            self._first = False
            code = "set(0, 'defaultfigurepaperunits', 'inches');"
            self._matlab.run_code(code)
            self._matlab.run_code("set(0, 'defaultfigureunits', 'inches');")
            self.handle_plot_settings()

        self.log.debug('execute: %s' % code)
        resp = self._matlab.run_code(code.strip())
        self.log.debug('execute done')
        if 'stdout' not in resp['content']:
            raise ValueError(resp)
        if 'figures' in resp['content']:
            for fname in resp['content']['figures']:
                try:
                    im = Image(filename=fname)
                    self.Display(im)
                except Exception as e:
                    self.Error(e)
        return resp['content']['stdout'].strip()

    def get_kernel_help_on(self, info, level=0, none_on_fail=False):
        obj = info.get('help_obj', '')
        if not obj or len(obj.split()) > 1:
            if none_on_fail:
                return None
            else:
                return ""
        return self.do_execute_direct('help %s' % obj)

    def handle_plot_settings(self):
        """Handle the current plot settings"""
        settings = self.plot_settings
        settings.setdefault('size', '560,420')

        if isinstance(settings['size'], tuple):
            width, height = settings['size']
        else:
            try:
                width, height = settings['size'].split(',')
                width, height = int(width), int(height)
            except Exception as e:
                self.Error(e)
                width, height = 560, 420

        cmd = "set(0, 'defaultfigurepapersize', [0 0 %s %s]);"
        self.do_execute_direct(cmd % (width, height))

    def repr(self, obj):
        return obj

if __name__ == '__main__':
    from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=MatlabKernel)
