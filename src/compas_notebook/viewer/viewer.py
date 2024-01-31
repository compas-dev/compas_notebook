from typing import Literal
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
        Width of the viewer scene.
    height : int, optional
        Height of the viewer scene.
    background : :class:`compas.colors.Color`, optional
        The background color of the scene.
    show_grid : bool, optional
        Show a grid in the scene.
    show_axes : bool, optional
        Show axes in the scene.
    show_toolbar : bool, optional
        Show the toolbar.
    viewport : {'top', 'left', 'front', 'perspective'}, optional
        The viewport of the viewer.

    Examples
    --------
    This example is meant to be run from within a Jupyter notebook.

    >>> import compas
    >>> from compas.datastructures import Mesh
    >>> from compas_notebook.viewer import Viewer
    >>> mesh = Mesh.from_obj(compas.get('tubemesh.obj'))
    >>> viewer = Viewer()
    >>> viewer.scene.add(mesh)  # doctest: +SKIP
    >>> viewer.show()        # doctest: +SKIP

    """

    def __init__(
        self,
        scene: Scene = None,
        camera: dict = None,
        width: int = 1100,
        height: int = 580,
        background: Color = None,
        show_grid: bool = True,
        show_axes: bool = True,
        show_toolbar: bool = True,
        viewport: Literal["top", "left", "front", "perspective"] = "perspective",
    ):
        aspect = width / height
        background = Color.coerce(background) or Color.from_hex("#eeeeee")
        camera = camera or {}

        self.width = width
        self.height = height
        self.viewport = viewport

        self.show_grid = show_grid
        self.show_axes = show_axes
        self.show_toolbar = show_toolbar

        self.scene = scene or Scene(context="Notebook")

        # scene

        self.scene3 = three.Scene(background=background.hex)

        if self.show_grid:
            grid = three.GridHelper(size=20, divisions=20, colorCenterLine=Color.grey().hex, colorGrid=Color.grey().lightened(50).hex)
            grid.rotateX(3.14159 / 2)
            self.scene3.add(grid)

        if self.show_axes:
            self.axes = three.AxesHelper(size=0.5)
            self.scene3.add(self.axes)

        # camera and controls

        if self.viewport == "top":
            self.camera3 = three.OrthographicCamera(width / -2, width / 2, height / 2, height / -2, 0.1, 10000)
            self.camera3.position = camera.get("position", [0, 0, 1])
            self.camera3.zoom = 1
            self.controls3 = three.OrbitControls(controlling=self.camera3)
            self.controls3.enableRotate = False

        elif self.viewport == "perspective":
            self.camera3 = three.PerspectiveCamera()
            self.camera3.position = camera.get("position", [0, -10, 5])
            self.camera3.up = camera.get("up", [0, 0, 1])
            self.camera3.aspect = aspect
            self.camera3.near = camera.get("near", 0.1)
            self.camera3.far = camera.get("far", 10000)
            self.camera3.fov = camera.get("fov", 50)
            self.camera3.lookAt(camera.get("target", [0, 0, 0]))
            self.controls3 = three.OrbitControls(controlling=self.camera3)

        else:
            raise NotImplementedError

        # renderer

        self.renderer3 = three.Renderer(
            scene=self.scene3,
            camera=self.camera3,
            controls=[self.controls3],
            width=width,
            height=height,
        )

        # ui

        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.ui = widgets.VBox()
        self.ui.layout.width = "auto"
        self.ui.layout.height = f"{self.height + 4 + 48}px" if self.show_toolbar else f"{self.height + 4}px"

        self.main = widgets.Box()
        self.main.layout.width = "auto"
        self.main.layout.height = f"{self.height + 4}px"
        self.main.children = [self.renderer3]

        self.toolbar = None
        if self.show_toolbar:
            self.toolbar = self.make_toolbar()
            self.ui.children = [self.toolbar, self.main]
        else:
            self.toolbar = None
            self.ui.children = [self.main]

    def make_toolbar(self):
        """Initialize the toolbar."""
        zoom_extents_button = widgets.Button(icon="square", tooltip="Zoom extents", layout=widgets.Layout(width="32px", height="32px"))
        zoom_extents_button.on_click(lambda x: self.zoom_extents())

        zoom_in_button = widgets.Button(icon="search-plus", tooltip="Zoom in", layout=widgets.Layout(width="32px", height="32px"))
        zoom_in_button.on_click(lambda x: self.zoom_in())

        zoom_out_button = widgets.Button(icon="search-minus", tooltip="Zoom out", layout=widgets.Layout(width="32px", height="32px"))
        zoom_out_button.on_click(lambda x: self.zoom_out())

        toolbar = widgets.HBox()
        toolbar.layout.display = "flex"
        toolbar.layout.flex_flow = "row"
        toolbar.layout.align_items = "center"
        toolbar.layout.width = "auto"
        toolbar.layout.height = "48px"
        toolbar.children = [zoom_extents_button, zoom_in_button, zoom_out_button]

        return toolbar

    def show(self):
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
            if hasattr(obj, "mesh"):
                box = Box.from_bounding_box(obj.mesh.aabb())
                xmin = min(xmin, box.xmin)
                ymin = min(ymin, box.ymin)
                zmin = min(zmin, box.zmin)
                xmax = max(xmax, box.xmax)
                ymax = max(ymax, box.ymax)
                zmax = max(zmax, box.zmax)
            elif hasattr(obj, "geometry"):
                pass
        dx = xmax - xmin
        dy = ymax - ymin
        dz = zmax - zmin
        cx = (xmax + xmin) / 2
        cy = (ymax + ymin) / 2
        cz = (zmax + zmin) / 2
        d = max(dx, dy, dz)

        if self.viewport == "perspective":
            self.camera3.position = [cx, cy - d, cz + 0.5 * d]
            self.camera3.lookAt([cx, cy, cz])
            self.camera3.zoom = 1
            self.controls3.target = [cx, cy, cz]

        elif self.viewport == "top":
            self.camera3.position = [cx, cy, cz + d]
            self.camera3.zoom = min(0.75 * self.width / d, 0.75 * self.height / d)
            self.controls3.target = [cx, cy, cz]

        else:
            raise NotImplementedError

    def zoom_in(self):
        """Zoom in."""
        self.camera3.zoom *= 2

    def zoom_out(self):
        """Zoom out."""
        self.camera3.zoom /= 2
