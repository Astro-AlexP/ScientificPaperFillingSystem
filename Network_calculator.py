import networkx as nx
import plotly.graph_objects as go
import numpy as np

def makeGraph(data, edges):
    node_data = {}

    nodeSize = []
    for size in data['PaperImpact']:
        if size == 0:
            size = 1
        Size = (45)/(1+(2.7**(3-0.01*size))) + 9

        nodeSize.append(Size)

    shapes = []
    for paper in data['Keywords']:
        shapes.append(markerShape(paper))

    colors = calcGradient(data['Year'])

    for i in range(len(data['id'])):
        node_data[data['id'][i]] = {'Title': data['Title'][i]}

    G = nx.Graph()
    G.add_nodes_from(node_data)
    G.add_edges_from(edges)

    G_temp = G.copy()
    dummy_id = "__CENTER_ANCHOR__"
    G_temp.add_node(dummy_id)

    for node in list(nx.isolates(G)):
        G_temp.add_edge(node, dummy_id)


    pos = nx.spring_layout(G_temp, seed=58)

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
        marker=dict(size=nodeSize, color=colors, symbol=shapes)
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

def markerShape(keywords):
    for word in keywords:
        if word.lower() == 'Review':
            return 'octagon'

        if word.lower() == 'textbook':
            return 'diamond'

        if word.lower() == 'thesis':
            return 'hexagon'

        if word.lower() == 'preprint':
            return 'pentagon'

        if word.lower() == 'paper':
            return 'circle'

        else:
            return 'square'


def calcGradient(years):
    minyear = min(years)
    maxyear = max(years)

    colors = []
    for year in years:
        pos = (maxyear - year) / (maxyear - minyear)
        colors.append(gradient(pos))

    return colors

def gradient(pos):
    start = np.array([0, 153, 255])
    end = np.array([255, 0, 47])

    color = np.round((end - start) * pos, 0)

    hexdec = '#' + str(hex(int(color[0]))[-2:]) + str(hex(int(color[1]))[-2:]) + str(hex(int(color[2]))[-2:])

    return hexdec
