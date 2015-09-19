A Jupyter/IPython kernel for Matlab

This requires IPython 3 and `pymatbridge <http://pypi.python.org/pypi/pymatbridge>`_.

To test it, install via ``pip`` or ``setup.py``, then::

    ipython qtconsole --kernel=matlab_kernel

Or select the Matlab Kernel in the IPython Notebook.

This is based on `MetaKernel <http://pypi.python.org/pypi/metakernel>`_,
which means it features a standard set of magics.

A sample notebook is available online_.

You can specify the path to your matlab executable by creating a `MATLAB_EXECUTABLE` environmental variable::

   MATLAB_EXECUTABLE=/usr/bin/matlab
   ipython notebook --kernel=matlab_kernel 

For example, on OSX, you could add something like the following to ~/.bash_profile::
  
   export MATLAB_EXECUTABLE=/Applications/MATLAB_2015b.app/bin/matlab

A note about plotting.  After each call to Matlab, we ask Matlab to save any 
open figures to image files whose format and resolution are defined using 
the `%plot` magic.  The resulting image is shown inline in the notebook.

.. _online: http://nbviewer.ipython.org/github/Calysto/matlab_kernel/blob/master/matlab_kernel.ipynb
