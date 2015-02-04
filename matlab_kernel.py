from __future__ import print_function

from metakernel import MetaKernel
from pymatbridge import Matlab
from IPython.display import Image


__version__ = '0.2'


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
            self.handle_plot_settings()

        self.log.debug('execute: %s' % code)
        resp = self._matlab.run_code(code.strip())
        self.log.debug('execute done')
        if 'stdout' not in resp['content']:
            raise ValueError(resp)
        if ('figures' in resp['content']
                and self.plot_settings.get('backend', None) == 'inline'):
            for fname in resp['content']['figures']:
                try:
                    im = Image(filename=fname)
                    self.Display(im)
                except Exception as e:
                    self.Error(e)
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

    def handle_plot_settings(self):
        """Handle the current plot settings"""
        settings = self.plot_settings
        if settings.get('format', None) is None:
            settings.clear()
        settings.setdefault('backend', 'inline')
        settings.setdefault('format', 'png')
        settings.setdefault('size', '560,420')

        cmds = []

        if settings['backend'] == 'inline':
            cmds.append("set(0, 'defaultfigurevisible', 'off');")
        else:
            cmds.append("set(0, 'defaultfigurevisible', 'on');")

        try:
            width, height = settings['size'].split(',')
            width, height = int(width), int(height)
        except Exception as e:
            self.Error(e)
            width, height = 560, 420

        cmds.append("""
        function make_figs(figdir)
            figHandles = get(0, 'children');
            for fig=1:length(figHandles)
                f = figHandles(fig);
                p = get(f, 'position');
                  w = %(width)s;
                  h = %(height)s;
                  if (p(3) > %(width)s);
                        h = p(4) * w / p(3);
                  end;
                  if (p(4) > %(height)s);
                        w = p(3) * h / p(4);
                  end;
                  size_fmt = sprintf('-S%%d,%%d', w, h);
                  outfile = fullfile(figdir, ['MatlabFig', sprintf('%%03d', fig)]);
                  print(f, outfile, '-d%(format)s', '-tight', size_fmt);
                close(fig);
            end;
        endfunction;
        """ % dict(width=width, height=height, format=settings['format']))

        cmds.append("set(0, 'DefaultFigurePosition', [300, 200, %s, %s]);" %
                    (width, height))

        self.do_execute_direct('\n'.join(cmds))

if __name__ == '__main__':
    from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=MatlabKernel)
