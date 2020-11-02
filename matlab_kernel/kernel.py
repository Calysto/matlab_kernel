try:
    import matlab.engine
    from matlab.engine import MatlabExecutionError
except ImportError:
    matlab = None
    class MatlabExecutionError(Exception):
        pass
from functools import partial
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import json
import os
import sys
try:
    from tempfile import TemporaryDirectory
except ImportError:
    from backports.tempfile import TemporaryDirectory

from IPython.display import Image
from metakernel import MetaKernel, ExceptionWrapper

try:
    from wurlitzer import pipes
except Exception:
    pipes = None

from . import __version__


class _PseudoStream:

    def __init__(self, writer):
        self.write = writer


def get_kernel_json():
    """Get the kernel json for the kernel.
    """
    here = os.path.dirname(__file__)
    with open(os.path.join(here, 'kernel.json')) as fid:
        data = json.load(fid)
    data['argv'][0] = sys.executable
    return data


class MatlabKernel(MetaKernel):
    app_name = 'matlab_kernel'
    implementation = "Matlab Kernel"
    implementation_version = __version__,
    language = "matlab"
    language_version = __version__,
    banner = "Matlab Kernel"
    language_info = {
        "mimetype": "text/x-octave",
        "codemirror_mode": "octave",
        "name": "matlab",
        "file_extension": ".m",
        "version": __version__,
        "help_links": MetaKernel.help_links,
    }
    kernel_json = get_kernel_json()

    def __init__(self, *args, **kwargs):
        super(MatlabKernel, self).__init__(*args, **kwargs)
        self.__matlab = None

    def get_usage(self):
        return "This is the Matlab kernel."

    @property
    def _matlab(self):
        if self.__matlab:
            return self.__matlab

        if matlab is None:
            raise ImportError("""
        Matlab engine not installed:
        See https://www.mathworks.com/help/matlab/matlab-engine-for-python.htm
        """)
        try:
            self.__matlab = matlab.engine.start_matlab()
        except matlab.engine.EngineError:
            self.__matlab = matlab.engine.connect_matlab()
        # detecting the correct kwargs for async running
        # matlab 'async' param is deprecated since it became a keyword in python 3.7
        # instead, 'background' param is available and recommended since Matlab R2017b
        self._async_kwargs = {'nargout': 0, 'async': True}
        try:
            self._matlab.eval('version', **self._async_kwargs)
        except SyntaxError:
            self._async_kwargs = {'nargout': 0, 'background': True}
        self._validated_plot_settings = {
            "backend": "inline",
            "size": (560, 420),
            "format": "png",
            "resolution": 96,
        }
        self._validated_plot_settings["size"] = tuple(
            self._matlab.get(0., "defaultfigureposition")[0][2:])
        self.handle_plot_settings()
        return self.__matlab

    def do_execute_direct(self, code):
        if pipes:
            retval = self._execute_async(code)
        else:
            retval = self._execute_sync(code)

        settings = self._validated_plot_settings
        if settings["backend"] == "inline":
            nfig = len(self._matlab.get(0., "children"))
            if nfig:
                with TemporaryDirectory() as tmpdir:
                    try:
                        self._matlab.eval(
                            "arrayfun("
                                "@(h, i) print(h, sprintf('{}/%06i', i), '-d{}', '-r{}'),"
                                "get(0, 'children'), ({}:-1:1)')".format(
                                    '/'.join(tmpdir.split(os.sep)),
                                    settings["format"],
                                    settings["resolution"],
                                    nfig),
                            nargout=0)
                        self._matlab.eval(
                            "arrayfun(@(h) close(h), get(0, 'children'))",
                            nargout=0)
                        for fname in sorted(os.listdir(tmpdir)):
                            self.Display(Image(
                                filename="{}/{}".format(tmpdir, fname)))
                    except Exception as exc:
                        self.Error(exc)

        return retval

    def get_kernel_help_on(self, info, level=0, none_on_fail=False):
        name = info.get("help_obj", "")
        out = StringIO()
        self._matlab.help(name, nargout=0, stdout=out)
        return out.getvalue()

    def get_completions(self, info):
        """Get completions from kernel based on info dict.
        """

        # Only MATLAB versions R2013a, R2014b, and R2015a were available for
        # testing.  This function is probably incompatible with some or many
        # other releases, as the undocumented features it relies on are subject
        # to change without notice.

        # grep'ing MATLAB R2014b for "tabcomplet" and dumping the symbols of
        # the ELF files that match suggests that the internal tab completion
        # is implemented in bin/glnxa64/libmwtabcompletion.so and called
        # from /bin/glnxa64/libnativejmi.so, which contains the function
        # mtFindAllTabCompletions. We can infer from MATLAB's undocumented
        # naming conventions that this function can be accessed as a method of
        # com.matlab.jmi.MatlabMCR objects.

        # Trial and error reveals likely function signatures for certain MATLAB
        # versions.
        # R2014b and R2015a:
        #   mtFindAllTabCompletions(String substring, int len, int offset)
        #   where `substring` is the string to be completed, `len` is the
        #   length of the string, and the first `offset` values returned by the
        #   engine are ignored.
        # R2013a (not supported due to lack of Python engine):
        #   mtFindAllTabCompletions(String substring, int offset [optional])
        name = info["obj"]
        compls = self._matlab.eval(
            "cell(com.mathworks.jmi.MatlabMCR()."
                 "mtFindAllTabCompletions('{}', {}, 0))"
            .format(name, len(name)))

        # For structs, we need to return `structname.fieldname` instead of just
        # `fieldname`, which `mtFindAllTabCompletions` does.

        if "." in name:
            prefix, _ = name.rsplit(".", 1)
            if self._matlab.eval("isstruct({})".format(prefix)):
                compls = ["{}.{}".format(prefix, compl) for compl in compls]

        return compls

    def do_is_complete(self, code):
        if self.parse_code(code)["magic"]:
            return {"status": "complete"}
        with TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test_complete.m")
            with open(path, mode='w') as f:
                f.write(code)
            self._matlab.eval(
                "try, pcode {} -inplace; catch, end".format(tmpdir),
                nargout=0)
            if os.path.exists(os.path.join(tmpdir, "test_complete.p")):
                return {"status": "complete"}
            else:
                return {"status": "incomplete"}

    def handle_plot_settings(self):
        raw = self.plot_settings
        settings = self._validated_plot_settings

        backends = {"inline": "off", "native": "on"}
        backend = raw.get("backend")
        if backend is not None:
            if backend not in backends:
                self.Error("Invalid backend, should be one of {}"
                           .format(sorted(list(backends))))
            else:
                settings["backend"] = backend

        size = raw.get("size")
        if size is not None:
            try:
                width, height = size
            except Exception as exc:
                self.Error(exc)
            else:
                settings["size"] = size
        if "width" in raw:
            width, height = settings["size"]
            raw.setdefault("width", width)
            raw.setdefault("height", height)
            settings["size"] = (raw["width"], raw["height"])

        resolution = raw.get("resolution")
        if resolution is not None:
            settings["resolution"] = resolution

        backend = settings["backend"]
        width, height = settings["size"]
        resolution = settings["resolution"]
        for k, v in {
                "defaultfigurevisible": backends[backend],
                "defaultfigurepaperpositionmode": "manual",
                "defaultfigurepaperposition":
                    matlab.double([0, 0, width / resolution, height / resolution]),
                "defaultfigurepaperunits": "inches"}.items():
            self._matlab.set(0., k, v, nargout=0)

    def repr(self, obj):
        return obj

    def restart_kernel(self):
        self._matlab.exit()
        try:
            self._matlab = matlab.engine.start_matlab()
        except matlab.engine.EngineError:
            # This isn't a true restart
            self._matlab = None  # disconnect from engine
            self._matlab = matlab.engine.connect_matlab()  # re-connect
            self._matlab.clear('all')  # clear all content
        self.__matlab = None

    def do_shutdown(self, restart):
        self._matlab.exit()
        return super(MatlabKernel, self).do_shutdown(restart)

    def _execute_async(self, code):
        try:
            with pipes(stdout=_PseudoStream(partial(self.Print, end="")),
                stderr=_PseudoStream(partial(self.Error, end=""))):
                future = self._matlab.eval(code, **self._async_kwargs)
                future.result()
        except (SyntaxError, MatlabExecutionError, KeyboardInterrupt) as exc:
            pass
            #stdout = exc.args[0]
            #return ExceptionWrapper("Error", -1, stdout)

    def _execute_sync(self, code):
        out = StringIO()
        err = StringIO()
        if not isinstance(code, str):
            code = code.encode('utf8')
        try:
            self._matlab.eval(code, nargout=0, stdout=out, stderr=err)
        except (SyntaxError, MatlabExecutionError) as exc:
            stdout = exc.args[0]
            self.Error(stdout)
            return ExceptionWrapper("Error", -1, stdout)
        stdout = out.getvalue()
        self.Print(stdout)


if __name__ == '__main__':
    try:
        from ipykernel.kernelapp import IPKernelApp
    except ImportError:
        from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=MatlabKernel)
