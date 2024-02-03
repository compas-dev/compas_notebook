from compas.scene import GeometryObject
from compas.colors import Color
from compas_notebook.conversions import polygon_to_threejs
from .sceneobject import ThreeSceneObject


class PolygonObject(ThreeSceneObject, GeometryObject):
    """Scene object for drawing polygons."""

    def draw(self, color: Color = None):
        """Draw the polygon associated with the scene object.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the polygon.

        Returns
        -------
        list[three.Mesh, three.LineSegments]
            List of pythreejs objects created.

        """
        color: Color = Color.coerce(color) or self.color
        contrastcolor: Color = color.darkened(50) if color.is_light else color.lightened(50)

        geometry = polygon_to_threejs(self.geometry)

        self._guids = self.geometry_to_objects(geometry, color, contrastcolor)
        return self.guids
