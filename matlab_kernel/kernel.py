from __future__ import print_function

import os
from metakernel import MetaKernel
from pymatbridge import Matlab, Octave
from IPython.display import Image

from . import __version__


class MatlabKernel(MetaKernel):
    implementation = 'Matlab Kernel'
    implementation_version = __version__,
    language = 'matlab'
    language_version = __version__,
    banner = "Matlab Kernel"
    language_info = {
        'mimetype': 'text/x-octave',
        'name': 'matlab',
        'file_extension': '.m',
        'version': __version__,
        'help_links': MetaKernel.help_links,
    }

    _first = True

    def __init__(self, *args, **kwargs):
        super(MatlabKernel, self).__init__(*args, **kwargs)
        if 'OCTAVE_EXECUTABLE' in os.environ:
            self._matlab = Octave(os.environ['OCTAVE_EXECUTABLE'])
        else:
            executable = os.environ.get('MATLAB_EXECUTABLE', 'matlab')
            self._matlab = Matlab(executable)
        self._matlab.start()

    def get_usage(self):
        return "This is the Matlab kernel."

    def do_execute_direct(self, code):
        if self._first:
            self._first = False
            fig_code = "set(0, 'defaultfigurepaperunits', 'inches');"
            self._matlab.run_code(fig_code)
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
        if not resp['success']:
            self.Error(resp['content']['stdout'].strip())
        else:
            stdout = resp['content']['stdout'].strip()
            if stdout:
                self.Print(stdout)

    def get_kernel_help_on(self, info, level=0, none_on_fail=False):
        obj = info.get('help_obj', '')
        if not obj or len(obj.split()) > 1:
            if none_on_fail:
                return None
            else:
                return ""
        code = 'help %s' % obj
        resp = self._matlab.run_code(code.strip())
        return resp['content']['stdout'].strip() or None

    def get_completions(self, info):
        """
        Get completions from kernel based on info dict.
        """
        if isinstance(self._matlab, Matlab):
            return
        code = 'completion_matches("%s")' % info['obj']
        resp = self._matlab.run_code(code.strip())
        return resp['content']['stdout'].strip().splitlines() or None

    def handle_plot_settings(self):
        """Handle the current plot settings"""
        settings = self.plot_settings
        settings.setdefault('size', '560,420')

        width, height = 560, 420
        if isinstance(settings['size'], tuple):
            width, height = settings['size']
        elif settings['size']:
            try:
                width, height = settings['size'].split(',')
                width, height = int(width), int(height)
            except Exception as e:
                self.Error(e)

        size = "set(0, 'defaultfigurepaperposition', [0 0 %s %s])\n;"
        self.do_execute_direct(size % (width / 150., height / 150.))

    def repr(self, obj):
        return obj

    def restart_kernel(self):
        """Restart the kernel"""
        self._matlab.stop()

    def do_shutdown(self, restart):
        self._matlab.stop()

if __name__ == '__main__':
    try:
        from ipykernel.kernelapp import IPKernelApp
    except ImportError:
        from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=MatlabKernel)
