********************************************************************************
Tutorial
********************************************************************************

The main purpose of :mod:`compas_notebook` is to visualise COMPAS objects in a Jupyter notebook.


Basic Usage
===========

Visualization is handled by creating a viewer inside a Jupyter notebook and adding objects to its scene.
The scene is an instance of :class:`compas.scene.Scene` that is preconfigured for ``context="Notebook"``,
and works the same way as any other COMPAS scene.

.. note::

    For more information on visualisation with scenes, see ...


.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas_notebook.viewer import Viewer

    mesh = Mesh.from_obj(compas.get('tubemesh.obj'))

    viewer = Viewer()
    viewer.scene.add(mesh)
    viewer.show()


Object Colors
=============

To change the color of an object, specify the color when adding the object to the scene.
You can use a COMPAS color object, or any of the following color specifications: hex, rgb1, rgb255.

.. code-block:: python

    viewer.scene.add(mesh, color=Color.red())
    viewer.scene.add(mesh, color='#ff0000')
    viewer.scene.add(mesh, color=(1.0, 0.0, 0.0))
    viewer.scene.add(mesh, color=(255, 0, 0))


Configuration
=============

The viewer can be configured to have a certain size and to have a specific background colour.

.. code-block:: python

    viewer = Viewer(width=600, height=400, background='#eeeeee')

The grid can be turned on or off.

.. code-block:: python

    viewer = Viewer(show_grid=False)


Viewports
=========

The viewer supports two viewports: "top" and "perspective".
The default is "perspective".
Currently, you can only set the viewport when creating the viewer.
It cannot be changed afterwards.

.. code-block:: python

    viewer = Viewer(viewport='top')

Note that in the top viewport, rotation controls are disabled.


Toolbar
=======

By default, the viewer has a toolbar with minimal functionality: zoom extents, zoom in, zoom out.
The toolbar is on by default, but can be turned off.

.. code-block:: python

    viewer = Viewer(show_toolbar=False)


Scene Export
============

Because the scene is an instance of :class:`compas.scene.Scene`, it can be exported to JSON.
This can be done manually or using the ``save`` button in the viewer.

The scene can be exported by itself

.. code-block:: python

    viewer.scene.to_json("scene.json")
    compas.json_dump(viewer.scene, "scene.json")


or as part of a larger session object.

.. code-block:: python

    compas.json_dump({"scene": viewer.scene, "...": "..."}, "session.json")


An exported scene can be loaded into a diferent notebook or visualised in a different visualisation context such as Rhino or Blender.

.. code-block:: python

    # different notebook

    import compas
    from compas_notebook.viewer import Viewer

    scene = compas.json_load("scene.json")
    viewer = Viewer(scene=scene)
    viewer.show()


.. code-block:: python

    # Rhino

    import compas

    scene = compas.json_load("scene.json")
    scene.draw()
