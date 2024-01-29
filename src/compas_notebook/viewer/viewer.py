import pythreejs as three
import ipywidgets as widgets
from IPython.display import display as ipydisplay
from compas.colors import Color
from compas.geometry import Box
from compas.scene import Scene


class Viewer:
    """Viewer for COMPAS geometry in Jupyter notebooks.

    Parameters
    ----------
    scene : :class:`compas.scene.Scene`, optional
        A scene object.
    camera : dict, optional
        A dictionary of camera parameters.
        Valid keys are ``position``, ``up``, ``near``, ``far``, ``fov``.
    width : int, optional
        Width of the viewer.
    height : int, optional
        Height of the viewer.
    background : :class:`compas.colors.Color`, optional
        The background color of the scene.
    show_grid : bool, optional
        Show a grid in the scene.

    Examples
    --------
    This example is meant to be run from within a Jupyter notebook.

    >>> import compas
    >>> from compas.datastructures import Mesh
    >>> from compas_notebook.viewer import Viewer
    >>> mesh = Mesh.from_obj(compas.get('tubemesh.obj'))
    >>> viewer = Viewer()
    >>> viewer.scene.add(mesh)  # doctest: +SKIP
    >>> viewer.display()        # doctest: +SKIP

    """

    def __init__(
        self,
        scene: Scene = None,
        camera: dict = None,
        width: int = 1118,
        height: int = 600,
        background: Color = None,
        show_grid: bool = False,
    ):
        aspect = width / height
        background = background or Color.from_hex("#eeeeee")
        camera = camera or {}

        self.scene = scene or Scene(context="Notebook")

        self.camera3 = three.PerspectiveCamera()
        self.camera3.position = camera.get("position", [0, -10, 0])
        self.camera3.up = camera.get("up", [0, 0, 1])
        self.camera3.aspect = aspect
        self.camera3.near = camera.get("near", 0.1)
        self.camera3.far = camera.get("far", 10000)
        self.camera3.fov = camera.get("fov", 50)
        self.camera3.lookAt([0, 0, 0])

        self.controls3 = three.OrbitControls(controlling=self.camera3)
        self.scene3 = three.Scene(background=background.hex)
        self.renderer3 = three.Renderer(
            scene=self.scene3,
            camera=self.camera3,
            controls=[self.controls3],
            width=width,
            height=height,
        )

        zoom_extents_button = widgets.Button(icon="square", tooltip="Zoom extents", layout=widgets.Layout(width="32px", height="32px"))
        zoom_extents_button.on_click(lambda x: self.zoom_extents())

        zoom_in_button = widgets.Button(icon="search-plus", tooltip="Zoom in", layout=widgets.Layout(width="32px", height="32px"))
        zoom_in_button.on_click(lambda x: self.zoom_in())

        zoom_out_button = widgets.Button(icon="search-minus", tooltip="Zoom out", layout=widgets.Layout(width="32px", height="32px"))
        zoom_out_button.on_click(lambda x: self.zoom_out())

        self.toolbar = widgets.HBox()
        self.toolbar.layout.display = "flex"
        self.toolbar.layout.flex_flow = "row"
        self.toolbar.layout.align_items = "center"
        self.toolbar.layout.width = "100%"
        self.toolbar.layout.height = "48px"
        self.toolbar.children = [zoom_extents_button, zoom_in_button, zoom_out_button]

        self.main = widgets.Box()
        self.main.layout.width = "100%"
        self.main.layout.height = f"{height + 4}px"
        self.main.children = [self.renderer3]

        self.ui = widgets.VBox()
        self.ui.layout.width = "100%"
        self.ui.layout.height = f"{height + 4 + 48}px"
        self.ui.children = [self.toolbar, self.main]

    def display(self):
        """Display the viewer in the notebook."""
        self.scene.draw()
        for o in self.scene.objects:
            for o3 in o.guids:
                self.scene3.add(o3)
        ipydisplay(self.ui)

    def zoom_extents(self):
        """Zoom to the extents of the scene."""
        xmin = ymin = zmin = +1e12
        xmax = ymax = zmax = -1e12
        for obj in self.scene.objects:
            box = Box.from_bounding_box(obj.mesh.aabb())
            xmin = min(xmin, box.xmin)
            ymin = min(ymin, box.ymin)
            zmin = min(zmin, box.zmin)
            xmax = max(xmax, box.xmax)
            ymax = max(ymax, box.ymax)
            zmax = max(zmax, box.zmax)
        dx = xmax - xmin
        dy = ymax - ymin
        dz = zmax - zmin
        cx = (xmax + xmin) / 2
        cy = (ymax + ymin) / 2
        cz = (zmax + zmin) / 2
        d = max(dx, dy, dz)
        self.camera3.position = [cx, cy - d, cz]
        self.camera3.lookAt([cx, cy, cz])
        self.controls3.target = [cx, cy, cz]
        self.camera3.zoom = 1

    def zoom_in(self):
        """Zoom in."""
        self.camera3.zoom *= 2

    def zoom_out(self):
        """Zoom out."""
        self.camera3.zoom /= 2
