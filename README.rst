A Jupyter/IPython kernel for Matlab


This requires `Jupyter Notebook <http://jupyter.readthedocs.org/en/latest/install.html>`_,
and the `Matlab engine for Python <https://www.mathworks.com/help/matlab/matlab-engine-for-python.html>`_.

To install::

    pip install matlab_kernel
    python -m matlab_kernel install

To use it, run one of:

.. code:: shell

    ipython notebook
    # In the notebook interface, select Matlab from the 'New' menu
    ipython qtconsole --kernel matlab
    ipython console --kernel matlab

This is based on `MetaKernel <http://pypi.python.org/pypi/metakernel>`_,
which means it features a standard set of magics.

A sample notebook is available online_.

A note about plotting.  After each call to Matlab, we ask Matlab to save any
open figures to image files whose format and resolution are defined using the
`%plot` magic.  The resulting image is shown inline in the notebook.  You can
use `%plot native` to raise normal MATLAB windows instead.

.. _online: http://nbviewer.ipython.org/github/Calysto/matlab_kernel/blob/master/matlab_kernel.ipynb
