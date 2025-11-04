from pathlib import Path
import graphviz

def build_simple_diagram(ccg: dict, out_path: Path):
    """
    Build a tiny Graphviz diagram from ccg nodes/edges and save as SVG.
    If ccg empty, produce a placeholder diagram.
    """
    dot = graphviz.Digraph(format='svg')
    nodes = ccg.get("nodes", [])
    edges = ccg.get("edges", [])
    if not nodes:
        dot.node("no", "No CCG data")
    else:
        # Add nodes
        for n in nodes[:50]:
            nid = n.get("id", "n")
            label = nid.split(":")[-1]
            dot.node(nid, label)
        # Add edges (edges use names, but in our simple CCg we have 'to' as function name)
        for e in edges[:200]:
            f = e.get("from")
            t = e.get("to")
            # try to find node with name endswith t
            target_nodes = [nd for nd in nodes if nd.get("id","").endswith(":"+t)]
            if target_nodes:
                dot.edge(f, target_nodes[0].get("id"))
            else:
                # create a target node for external reference
                t_id = f"ext:{t}"
                dot.node(t_id, t)
                dot.edge(f, t_id)
    out = dot.render(filename=str(out_path.with_suffix('')), cleanup=True)
    # graphviz.render returns path
    return out
