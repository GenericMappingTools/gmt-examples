Contributors Guide
------------------

This is a community driven project and everyone is welcome to contribute. The
project is hosted at the `gmt-examples GitHub repository <https://github.com/GenericMappingTools/gmt-examples>`_.

The goal is to maintain a diverse community that's pleasant for everyone.
**Please be considerate and respectful of others**. Everyone must abide by our
`Code of Conduct <https://github.com/GenericMappingTools/gmt-examples/blob/main/CODE_OF_CONDUCT.md>`_
and we encourage all to read it carefully.

GMT Examples Overview
~~~~~~~~~~~~~~~~~~~~~

There are two main components to GMT examples project:

* Gallery examples, with source material in the ``docs/gallery/`` folder.
* Tutorial examples, with source material in the ``docs/tutorials/`` folder.

The gallery examples are designed to instruct users on how to complete a specific
problem. For general recommendations on how to design effective gallery examples,
see the `diataxis framework's section on how-to guides <https://diataxis.fr/how-to-guides/>`_.

The tutorials are learning orientated with the goal of teaching users GMT. For
general recommendations on how to design effective tutorials, see the
`diataxis framework's section on tutorials <https://diataxis.fr/tutorials/>`_.

The documentation are written primarily in
`reStructuredText <https://docutils.sourceforge.io/rst.html>`_ and built by
`Sphinx <http://www.sphinx-doc.org/>`_. Please refer to
:gmt-module:`reStructuredText cheatsheet <devdocs/rst-cheatsheet.html>` if you are new to reStructuredText.

Setting up your environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following dependencies are required for building the GMT examples pages:

- `gmt <https://docs.generic-mapping-tools.org/latest/>`_ (GMT is required for executing example scripts)
- `sphinx <http://www.sphinx-doc.org/>`_ (a Python documentation generator for creating the docs from source files)
- `sphinx_gmt <https://www.generic-mapping-tools.org/sphinx_gmt/latest/>`_ (a Sphinx extension for creating GMT figures to accompany example scripts)
- `sphinx_rtd_theme <https://sphinx-rtd-theme.readthedocs.io/en/stable/>`_ (a Sphinx theme used for consistent documentation appearance between GMT projects)

Two options for installing the dependencies are :ref:`pip <Pip Setup>` and :ref:`conda <Conda Setup>`.
Since Sphinx is a Python documentation generator, you will need a working Python
environment. For those who do not already have a working Python environment,
one option is to use the minimal installer for Conda `Miniforge <https://github.com/conda-forge/miniforge>`_
along with the :ref:`conda <Conda Setup>` instructions.

Pip Setup
^^^^^^^^^

These instructions rely on the `pip <https://pip.pypa.io/en/stable/>`_ package
installer, which can be used to install all dependencies except GMT.
Follow the `GMT Install Guide <https://github.com/GenericMappingTools/gmt/blob/master/INSTALL.md>`_
to install GMT. The Python dependencies can be installed using the
``requirements.txt`` from the base of the repository (you may wish to setup a
`virtual environment <https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment>`_ first):

Unix/macOS::

  python -m pip install -r requirements.txt

Windows::

  py -m pip install -r requirements.txt

Conda Setup
^^^^^^^^^^^

These instructions rely on the `conda <https://docs.conda.io/en/latest/>`_ package
manager. Run the following from the base of the repository to create a new conda
environment from the ``environment.yml`` file::

  conda env create

Before building the documentation, you have to activate the environment
(you'll need to do this every time you start a new terminal)::

  conda activate gmt-examples

Building the documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have :ref:`setup your environment <Setting up your environment>`, you can
build the documentation using::

  cd docs
  make html

Contributing New Examples
~~~~~~~~~~~~~~~~~~~~~~~~~

The source files for the gallery examples and tutorials are ``.rst`` files in
``docs/`` that generate one or more figures using the
`sphinx_gmt <https://www.generic-mapping-tools.org/sphinx_gmt/latest/)>`_
extension. To add a new gallery example or tutorial:

* If necessary, create a new sub-directory under ``docs/gallery/`` for a
  gallery example section (e.g., ``basemaps/`` or ``plot_embellishments/``).
* Create a new ``.rst`` file inside the appropriate sub-directory in
  ``docs/gallery/`` or ``docs/tutorials/``.
* Add a descriptive title and as much explanation as necessary.
* Add hyperlinks to GMT modules using the ``gmt-module`` reStructuredText directive::

  :gmt-module:`grdview`

* Add hyperlinks to GMT module options by appending lower-case ``#<option>`` to
  the ``gmt-module`` argument::

  :gmt-module:`grdview#q`

* Add as many figures as needed using the ``gmtplot`` directive:

  ::

    .. gmtplot::

       gmt begin basemap png
         gmt basemap -B -Rg -JH5c
       gmt end show

  The figures will be placed after the source code in the built documentation
  by the ``sphinx_gmt`` extension.

* Add the file to the appropriate section in ``docs/index.rst`` using the following
  template:

  ::

    ```bash
      -  .. image:: _images/<file-name>-gmtplot-0.png
            :target: gallery/<section>/<file-name>.html
            :width: 80%
            :align: center

         :doc:`gallery/<section>/<file-name>`
    ```

  Edit the number in the ``.. image:: ...`` line to show a different figure on the
  index page.
