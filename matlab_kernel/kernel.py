from __future__ import print_function

import os
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
from metakernel import MetaKernel
from IPython.display import Image
try:
    import matlab.engine
    from matlab.engine import MatlabExecutionError
    matlab_native = True
except ImportError:
    from pymatbridge import Matlab, Octave
    matlab_native = False

from . import __version__


class MatlabEngine(object):

    def __init__(self):
        if 'OCTAVE_EXECUTABLE' in os.environ:
            self._engine = Octave(os.environ['OCTAVE_EXECUTABLE'])
            self._engine.start()
            self.name = 'octave'
        elif matlab_native:
            self._engine = matlab.engine.start_matlab()
            self.name = 'matlab'
        else:
            executable = os.environ.get('MATLAB_EXECUTABLE', 'matlab')
            self._engine = Matlab(executable)
            self._engine.start()
            self.name = 'pymatbridge'
        # add MATLAB-side helper functions to MATLAB's path
        if self.name != 'octave':
            kernel_path = os.path.dirname(os.path.realpath(__file__))
            toolbox_path = os.path.join(kernel_path, 'toolbox')
            self.run_code("addpath('%s');" % toolbox_path)

    def run_code(self, code):
        if matlab_native:
            return self._run_native(code)
        return self._engine.run_code(code)

    def stop(self):
        if matlab_native:
            self._engine.exit()
        else:
            self._engine.stop()

    def _run_native(self, code):
        out = StringIO()
        err = StringIO()
        if sys.version_info[0] < 3:
            code = str(code)
        try:
            self._engine.eval(code, nargout=0, stdout=out, stderr=err)
        except (SyntaxError, MatlabExecutionError) as exc:
            return dict(success=False, content=dict(stdout=exc.args[0]))
        return dict(success=True, content=dict(stdout=out.getvalue()))


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
        self._matlab = MatlabEngine()

    def get_usage(self):
        return "This is the Matlab kernel."

    def do_execute_direct(self, code):
        if self._first:
            self._first = False
            self.handle_plot_settings()

        self.log.debug('execute: %s' % code)
        resp = self._matlab.run_code(code.strip())
        self.log.debug('execute done')
        if 'stdout' not in resp['content']:
            raise ValueError(resp)
        backend = self.plot_settings['backend']
        if 'figures' in resp['content'] and backend == 'inline':
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
        if self._matlab.name != 'octave':
            code = "do_matlab_complete('%s')" % info['obj']
        else:
            code = 'do_complete("%s")' % info['obj']
        resp = self._matlab.run_code(code.strip())
        return resp['content']['stdout'].strip().splitlines() or []

    def handle_plot_settings(self):
        """Handle the current plot settings"""
        settings = self.plot_settings
        settings.setdefault('size', (560, 420))
        settings.setdefault('backend', 'inline')

        width, height = 560, 420
        if isinstance(settings['size'], tuple):
            width, height = settings['size']
        elif settings['size']:
            try:
                width, height = settings['size'].split(',')
                width, height = int(width), int(height)
                settings['size'] = width, height
            except Exception as e:
                self.Error(e)

        if settings['backend'] == 'inline':
            code = ["set(0, 'defaultfigurevisible', 'off')"]
        else:
            code = ["set(0, 'defaultfigurevisible', 'on')"]
        paper_size = "set(0, 'defaultfigurepaperposition', [0 0 %s %s])"
        figure_size = "set(0, 'defaultfigureposition', [0 0 %s %s])"
        code += ["set(0, 'defaultfigurepaperunits', 'inches')",
                 "set(0, 'defaultfigureunits', 'inches')",
                 paper_size % (int(width) / 150., int(height) / 150.),
                 figure_size % (int(width) / 150., int(height) / 150.)]
        if sys.platform == 'darwin' and self._matlab.name == 'octave':
            code + ['setenv("GNUTERM", "X11")']
            if settings['backend'] != 'inline':
                code += ["graphics_toolkit('%s');" % settings['backend']]
        self._matlab.run_code(';'.join(code))

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
