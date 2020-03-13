
A Matlab kernel for Jupyter
===========================

Prerequisites
-------------
Install `Jupyter Notebook <http://jupyter.readthedocs.org/en/latest/install.html>`_ and the
`Matlab engine for Python <https://www.mathworks.com/help/matlab/matlab-engine-for-python.html>`_.

Installation
------------

Install using::

    $ pip install matlab_kernel

or ``pip install git+https://github.com/Calysto/matlab_kernel`` for the dev version.

To use the kernel, run one of::

    $ jupyter notebook
    # In the notebook interface, select Matlab from the 'New' menu
    $ jupyter qtconsole --kernel matlab
    $ jupyter console --kernel matlab

To remove from kernel listings::

    $ jupyter kernelspec remove matlab


Configuration
-------------
The kernel can be configured by adding an ``matlab_kernel_config.py`` file to the
``jupyter`` config path.  The ``MatlabKernel`` class offers ``plot_settings`` as a configurable traits.
The available plot settings are:
'format', 'backend', 'width', 'height', and 'resolution'.

.. code:: bash

    cat ~/.jupyter/matlab_kernel_config.py
    c.MatlabKernel.plot_settings = dict(format='svg')


Troubleshooting
---------------

Kernel Times Out While Starting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If the kernel is not starting, try running the following from a terminal.

.. code:: shell

  python -m matlab_kernel.check

Please include that output if opening an issue.


Kernel is Not Listed
~~~~~~~~~~~~~~~~~~~~
If the kernel is not listed as an available kernel, first try the following command:

.. code:: shell

    python -m matlab_kernel install --user

If the kernel is still not listed, verify that the following point to the same
version of python:

.. code:: shell

    which python  # use "where" if using cmd.exe
    which jupyter


Additional information
----------------------

The Matlab kernel is based on `MetaKernel <http://pypi.python.org/pypi/metakernel>`_,
which means it features a standard set of magics.  For a full list of magics,
run ``%lsmagic`` in a cell.

A sample notebook is available online_.

A note about plotting.  After each call to Matlab, we ask Matlab to save any
open figures to image files whose format and resolution are defined using the
``%plot`` magic.  The resulting image is shown inline in the notebook.  You can
use ``%plot native`` to raise normal Matlab windows instead.


Advanced Installation Notes
---------------------------

We automatically install a Jupyter kernelspec when installing the python package. This location can be found using ``jupyter kernelspec list``. If the default location is not desired, you can remove the directory for the octave kernel, and install using ``python -m matlab_kernel install``. See ``python -m matlab_kernel install --help`` for available options.

It has been reported that Matlab version 2016b works fine. However, Matlab 2014b does not work with Python 3.5.

.. _online: http://nbviewer.ipython.org/github/Calysto/matlab_kernel/blob/master/matlab_kernel.ipynb


Development
~~~~~~~~~~~

Install the package locally::

    $ pip install -e .
    $ python -m matlab_kernel install

As you make changes, test them in a notebook (restart the kernel between changes).

