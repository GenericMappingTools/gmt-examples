# Contributors Guide

This is a community driven project and everyone is welcome to contribute. The
project is hosted at the [gmt-examples GitHub repository](https://github.com/GenericMappingTools/gmt-examples).

The goal is to maintain a diverse community that's pleasant for everyone.
**Please be considerate and respectful of others**. Everyone must abide by our
[Code of Conduct](https://github.com/GenericMappingTools/gmt-examples/blob/main/CODE_OF_CONDUCT.md)
and we encourage all to read it carefully.

## Setting up your environment

We highly recommend using [Anaconda](https://www.anaconda.com/download/) and the `conda`
package manager to install and manage your packages.


The repository includes a conda environment file `environment.yml` with the
specification for all development requirements to build and test the project.
See the [`environment.yml`](https://github.com/GenericMappingTools/gmt-examples/blob/main/environment.yml)
file for the list of dependencies and the environment name (`gmt-examples`).
Once you have forked and cloned the repository to your local machine, you can
use this file to create an isolated environment on which you can work.
Run the following on the base of the repository to create a new conda
environment from the `environment.yml` file:

```bash
conda env create
```

Before building and testing the project, you have to activate the environment
(you'll need to do this every time you start a new terminal):

```bash
conda activate gmt-examples
```

## Building the documentation

Once you have [setup your environment](#setting-up-your-environment), you can
build the documentation using:

```bash
    cd docs
    make html
```

## GMT Examples Overview

There are two main components to GMT examples project:

* Gallery examples, with source material in the `docs/examples/gallery/` folder.
* Tutorial examples, with source material in the `docs/examples/tutorials/` folder.

The gallery examples are designed to instruct users on how to complete a specific
problem. For general recommendations on how to design effective gallery examples,
see the [diataxis framework's section on how-to guides](https://diataxis.fr/how-to-guides/).

The tutorials are learning orientated with the goal of teaching users GMT. For
general recommendations on how to design effective tutorials, see the
[diataxis framework's section on tutorials](https://diataxis.fr/tutorials/).

The documentation are written primarily in
[reStructuredText](https://docutils.sourceforge.io/rst.html) and built by
[Sphinx](http://www.sphinx-doc.org/). Please refer to
[reStructuredText Cheatsheet](https://docs.generic-mapping-tools.org/latest/devdocs/rst-cheatsheet.html)
if you are new to reStructuredText.

## Contributing New Examples

The source files for the gallery examples and tutorials are `.rst` files in
`docs/examples/` that generate one or more figures using the
[sphinx_gmt](https://www.generic-mapping-tools.org/sphinx_gmt/latest/)
extension. To add a new gallery example or tutorial:

* If necessary, create a new sub-directory under `docs/examples/gallery/` for a
  gallery example section (e.g., `basemaps/` or `plot_embellishments/`).
* Create a new `.rst` file inside the appropriate sub-directory in
  `docs/examples/gallery/` or `docs/examples/tutorials/`.
* Add a descriptive title and as much explanation as necessary.
* Add hyperlinks to GMT modules using the `gmt-module` restructured text directive:

  ```bash
  :gmt-module:`grdview`
  ```

* Add hyperlinks to GMT module options by appending lower-case `#<option>` to
  the `gmt-module` argument:

  ```bash
  :gmt-module:`grdview#q`
  ```

* Add as many figures as needed using the `gmtplot` directive:

  ```bash
  .. gmtplot::
     :language: bash

     gmt begin basemap png
        gmt basemap -B -Rg -JH5c
     gmt end show

  ```

  The figures will be placed after the source code in the built documentation
  by the `sphinx_gmt` extension.

* Add the file to the appropriate section in `docs/index.rst` using the following
  template:

  ```bash
    -  .. image:: _images/<file-name>-gmtplot-0.png
        :target: examples/gallery/<section>/<file-name>.html
        :width: 80%
        :align: center

     :doc:`examples/gallery/<section>/<file-name>`
  ```

  Edit the number in the `.. image:: ...` line to show a different figure on the
  index page.
