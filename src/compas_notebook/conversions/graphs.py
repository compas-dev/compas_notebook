import numpy
import pythreejs as three


def nodes_and_edges_to_threejs(nodes: list[list[float]], edges: list[tuple[int, int]]) -> three.BufferGeometry:
    """Convert nodes and edges to a PyThreeJS geometry.

    Parameters
    ----------
    nodes
        List of nodes.
    edges
        List of edges.

    Returns
    -------
    three.BufferGeometry
        The PyThreeJS geometry.

    """
    nodes = numpy.array(nodes, dtype=numpy.float32)  # type: ignore
    edges = numpy.array(edges, dtype=numpy.uint32).ravel()  # type: ignore

    geometry = three.BufferGeometry(
        attributes={
            "position": three.BufferAttribute(nodes, normalized=False),
            "index": three.BufferAttribute(edges, normalized=False, itemSize=2),
        }
    )

    return geometry


def nodes_to_threejs(nodes: list[list[float]]) -> three.BufferGeometry:
    """Convert nodes to a PyThreeJS geometry.

    Parameters
    ----------
    nodes
        List of nodes.

    Returns
    -------
    three.BufferGeometry
        The PyThreeJS geometry.

    """
    nodes = numpy.array(nodes, dtype=numpy.float32)  # type: ignore
    geometry = three.BufferGeometry(attributes={"position": three.BufferAttribute(nodes, normalized=False)})
    return geometry
