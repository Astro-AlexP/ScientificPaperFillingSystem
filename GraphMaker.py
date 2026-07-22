import networkx as nx
import plotly.graph_objects as go
#import
import numpy as np

def makeGraph(data, edges):
    node_data = {}

    nodeSize = []
    for size in data['PaperImpact']:
        if size == 0:
            size = 1
        tempSize = 7*np.log(size**2)-50
        if tempSize <= 10:
            nodeSize.append(10)

        else:
            nodeSize.append(tempSize)

    for i in range(len(data['id'])):
        node_data[data['id'][i]] = {'Title': data['Title'][i]}

    G = nx.Graph()
    G.add_nodes_from(node_data)
    G.add_edges_from(edges)

    # 1. Create a clone graph and inject a central anchor node
    G_temp = G.copy()
    dummy_id = "__CENTER_ANCHOR__"
    G_temp.add_node(dummy_id)

    # 2. Tie every isolated node to the anchor
    for node in list(nx.isolates(G)):
        G_temp.add_edge(node, dummy_id)

    # 3. Compute layout (the springs will pull isolates toward the center)
    pos = nx.spring_layout(G_temp, seed=58)

    # 4. Erase the dummy node's coordinates so it doesn't render in Plotly
    if dummy_id in pos:
        del pos[dummy_id]

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    # 4. Extract Node Coordinates
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        customdata=data['id'],
        hovertext=data['Title'],
        hoverinfo='text',
        #text=[str(node) for node in G.nodes()],
        textposition="top center",
        marker=dict(size=nodeSize, color='SkyBlue')
    )

    # 5. Plot the graph
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        margin=dict(l=10, r=10, t=10, b=10),
                        autosize=True,
                        showlegend=False,
                        hovermode='closest',
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))


    return fig