
A Matlab kernel for Jupyter
===========================

Prerequisites: Install `Jupyter Notebook <http://jupyter.readthedocs.org/en/latest/install.html>`_ and the 
`Matlab engine for Python <https://www.mathworks.com/help/matlab/matlab-engine-for-python.html>`_.

To install::

    $ pip install matlab_kernel
    # or `pip install git+https://github.com/Calysto/matlab_kernel`
    # for the devel version.

To use it, run one of::

    $ jupyter notebook
    # In the notebook interface, select Matlab from the 'New' menu
    $ jupyter qtconsole --kernel matlab
    $ jupyter console --kernel matlab
    
To remove from kernel listings::

    $ jupyter kernelspec remove matlab
    
Additional information::

The Matlab kernel is based on `MetaKernel <http://pypi.python.org/pypi/metakernel>`_,
which means it features a standard set of magics.

A sample notebook is available online_.

A note about plotting.  After each call to Matlab, we ask Matlab to save any
open figures to image files whose format and resolution are defined using the
``%plot`` magic.  The resulting image is shown inline in the notebook.  You can
use ``%plot native`` to raise normal Matlab windows instead.


Advanced Installation Notes:: 

We automatically install a Jupyter kernelspec when installing the python package. This location can be found using ``jupyter kernelspec list``. If the default location is not desired, you can remove the directory for the octave kernel, and install using python -m matlab_kernel install. See python -m matlab_kernel install --help for available options.


.. _online: http://nbviewer.ipython.org/github/Calysto/matlab_kernel/blob/master/matlab_kernel.ipynb

It has been reported that Matlab version 2016b works fine. However, Matlab 2014b does not work with Python 3.5. 
