
A Matlab kernel for Jupyter
===========================

Prerequisites: Install `Jupyter Notebook <http://jupyter.readthedocs.org/en/latest/install.html>`_ and the 
`Matlab engine for Python <https://www.mathworks.com/help/matlab/matlab-engine-for-python.html>`_.

To install::

    $ pip install matlab_kernel
    # or `pip install git+https://github.com/Calysto/matlab_kernel`
    # for the devel version.
    $ python -m matlab_kernel install

To use it, run one of::

    $ jupyter notebook
    # In the notebook interface, select Matlab from the 'New' menu
    $ jupyter qtconsole --kernel matlab
    $ jupyter console --kernel matlab

This is based on `MetaKernel <http://pypi.python.org/pypi/metakernel>`_,
which means it features a standard set of magics.

A sample notebook is available online_.

A note about plotting.  After each call to Matlab, we ask Matlab to save any
open figures to image files whose format and resolution are defined using the
``%plot`` magic.  The resulting image is shown inline in the notebook.  You can
use ``%plot native`` to raise normal Matlab windows instead.

.. _online: http://nbviewer.ipython.org/github/Calysto/matlab_kernel/blob/master/matlab_kernel.ipynb
