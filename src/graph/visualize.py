import plotly.graph_objects as go


def visualize_graph(graph, path=None, title="Graph Visualization"):
    """
    Visualize a graph using Plotly with interactive nodes and edges.
    Shows each user and lines connecting them to their followers.

    Args:
        graph: Dictionary where keys are users and values are lists of followed users
        path: Optional list of users representing a path to highlight
        title: Plot title
    """
    if not graph:
        print("No graph data to visualize.")
        return

    # Collect all nodes
    nodes = set(graph.keys())
    for follows in graph.values():
        nodes.update(follows)
    nodes = list(nodes)

    # Position nodes using a simple circular layout
    import math
    n = len(nodes)
    node_positions = {}
    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / n - math.pi / 2
        node_positions[node] = (math.cos(angle), math.sin(angle))

    # Create edge coordinates: follower -> user (who follows whom)
    edge_x, edge_y = [], []
    for user, follower_list in graph.items():
        if user in node_positions:
            for follower in follower_list:
                if follower in node_positions:
                    # Edge from follower to user
                    edge_x.extend([node_positions[follower][0], node_positions[user][0], None])
                    edge_y.extend([node_positions[follower][1], node_positions[user][1], None])

    # Create edge trace
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines',
        name='Connections'
    )

    # Create node trace
    node_x, node_y, node_text = [], [], []
    for node in nodes:
        x, y = node_positions[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition='middle center',
        textfont=dict(size=10, color='black'),
        marker=dict(
            size=15,
            color='#1f77b4',
            line=dict(color='white', width=2)
        ),
        name='Nodes'
    )

    # Highlight path if provided
    if path:
        path_x, path_y = [], []
        for node in path:
            if node in node_positions:
                x, y = node_positions[node]
                path_x.append(x)
                path_y.append(y)

        if path_x:
            path_trace = go.Scatter(
                x=path_x, y=path_y,
                mode='markers+lines',
                line=dict(width=3, color='red'),
                marker=dict(size=20, color='red'),
                hoverinfo='text',
                text=path,
                name='Path'
            )
            fig = go.Figure(data=[path_trace, node_trace, edge_trace])
        else:
            fig = go.Figure(data=[node_trace, edge_trace])
    else:
        fig = go.Figure(data=[node_trace, edge_trace])

    # Update layout
    fig.update_layout(
        title=title,
        showlegend=True,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        height=600
    )

    fig.show()
