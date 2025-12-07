import numpy
import pythreejs as three
from compas.geometry import Polygon
from compas.geometry import earclip_polygon


def vertices_and_faces_to_threejs(vertices: list[list[float]], faces: list[list[int]]) -> three.BufferGeometry:
    """Convert vertices and faces to a PyThreeJS geometry.

    Parameters
    ----------
    vertices
        List of vertices.
    faces
        List of faces.

    Returns
    -------
    three.BufferGeometry
        The PyThreeJS geometry.

    """
    triangles = []
    for face in faces:
        if len(face) == 3:
            triangles.append(face)
        elif len(face) == 4:
            triangles.append([face[0], face[1], face[2]])
            triangles.append([face[0], face[2], face[3]])
        else:
            polygon = Polygon([vertices[v] for v in face])
            ears = earclip_polygon(polygon)
            for ear in ears:
                triangles.append([face[index] for index in ear])

    vertices = numpy.array(vertices, dtype=numpy.float32)  # type: ignore
    triangles = numpy.array(triangles, dtype=numpy.uint32).ravel()  # type: ignore

    geometry = three.BufferGeometry(
        attributes={
            "position": three.BufferAttribute(vertices, normalized=False),
            "index": three.BufferAttribute(triangles, normalized=False, itemSize=3),
        }
    )

    return geometry


def vertices_and_edges_to_threejs(vertices: list[list[float]], edges: list[tuple[int, int]]) -> three.BufferGeometry:
    """Convert vertices and edges to a PyThreeJS geometry.

    Parameters
    ----------
    vertices
        List of vertices.
    edges
        List of edges.

    Returns
    -------
    three.BufferGeometry
        The PyThreeJS geometry.

    """
    vertices = numpy.array(vertices, dtype=numpy.float32)  # type: ignore
    edges = numpy.array(edges, dtype=numpy.uint32).ravel()  # type: ignore

    geometry = three.BufferGeometry(
        attributes={
            "position": three.BufferAttribute(vertices, normalized=False),
            "index": three.BufferAttribute(edges, normalized=False, itemSize=2),
        }
    )

    return geometry


def vertices_to_threejs(vertices: list[list[float]]) -> three.BufferGeometry:
    """Convert vertices to a PyThreeJS geometry.

    Parameters
    ----------
    vertices
        List of vertices.

    Returns
    -------
    three.BufferGeometry
        The PyThreeJS geometry.

    """
    vertices = numpy.array(vertices, dtype=numpy.float32)  # type: ignore
    geometry = three.BufferGeometry(attributes={"position": three.BufferAttribute(vertices, normalized=False)})
    return geometry
