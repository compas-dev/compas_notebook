********************************************************************************
Tutorial
********************************************************************************

The main purpose of :mod:`compas_notebook` is to visualise COMPAS objects in a Jupyter notebook.

Basics
======

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas_notebook.viewer import Viewer

    mesh = Mesh.from_obj(compas.get('tubemesh.obj'))

    viewer = Viewer()
    viewer.scene.add(mesh)
    viewer.show()
