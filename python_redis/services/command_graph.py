import python_redis.protocols.graph_protocols as graph_protocols

execute_task_graph = {
    graph_protocols.AddEdgeCommand: graph_protocols.GRAPH_TASKS.task_add_edge_command,
    graph_protocols.AddVertexCommand: graph_protocols.GRAPH_TASKS.task_add_vertex_command,
    graph_protocols.RemoveEdgeCommand: graph_protocols.GRAPH_TASKS.task_remove_edge_command,
    graph_protocols.RemoveVertexCommand: graph_protocols.GRAPH_TASKS.task_remove_vertex_command,
    graph_protocols.BFSCommand: graph_protocols.GRAPH_TASKS.task_bfs_command,
    graph_protocols.DFSCommand: graph_protocols.GRAPH_TASKS.task_dfs_command,
    graph_protocols.IsDirectedCommand: graph_protocols.GRAPH_TASKS.task_is_directed_command,
    graph_protocols.IsWeightedCommand: graph_protocols.GRAPH_TASKS.task_is_weighted_command,
    graph_protocols.DisplayCommand: graph_protocols.GRAPH_TASKS.task_display_command,
    graph_protocols.GetVertexCommand: graph_protocols.GRAPH_TASKS.task_get_vertex_by_value_command,
    graph_protocols.GetVerticesCommand: graph_protocols.GRAPH_TASKS.task_get_vertices_command,
    graph_protocols.GetEdgesByVertexCommand: graph_protocols.GRAPH_TASKS.task_get_edges_by_vertex_command,
    graph_protocols.GetKeyCommand: graph_protocols.GRAPH_TASKS.task_get_key_command,
    graph_protocols.SetKeyCommand: graph_protocols.GRAPH_TASKS.task_set_key_command,
    graph_protocols.DijkistraDistDictionaryCommand: graph_protocols.GRAPH_TASKS.task_dijkistra_dist_dict_command,
    graph_protocols.DijkistraPrevDictionaryCommand: graph_protocols.GRAPH_TASKS.task_dijkistra_prev_dict_command,
    graph_protocols.DijkistraShortestPathCommand: graph_protocols.GRAPH_TASKS.task_dijkistra_shortest_path_command,
}
execute_command_graph = {
    graph_protocols.COMMAND_SET_KEY: graph_protocols.execute_set_key_command,
    graph_protocols.COMMAND_GET_KEY: graph_protocols.execute_get_key_command,
    graph_protocols.COMMAND_BFS: graph_protocols.execute_breadth_first_search_command,
    graph_protocols.COMMAND_DFS: graph_protocols.execute_depth_first_search_command,
    graph_protocols.COMMAND_ADD_VERTEX: graph_protocols.execute_add_vertex_command,
    graph_protocols.COMMAND_ADD_EDGE: graph_protocols.execute_add_edge_command,
    graph_protocols.COMMAND_REMOVE_VERTEX: graph_protocols.execute_remove_vertex_by_value_command,
    graph_protocols.COMMAND_REMOVE_EDGE: graph_protocols.execute_remove_edge_command,
    graph_protocols.COMMAND_IS_WEIGHTED: graph_protocols.execute_is_weighted_command,
    graph_protocols.COMMAND_IS_DIRECTED: graph_protocols.execute_is_directed_command,
    graph_protocols.COMMAND_SHOW: graph_protocols.execute_display_command,
    graph_protocols.COMMAND_GET_VERTEX_BY_VALUE: graph_protocols.execute_get_vertex_by_value_command,
    graph_protocols.COMMAND_GET_VERTICES: graph_protocols.execute_get_vertices_command,
    graph_protocols.COMMAND_GET_VERTEX_EDGE: graph_protocols.execute_get_edges_by_vertex_command,
    graph_protocols.COMMAND_DIJKISTRA_DIST_DICT: graph_protocols.execute_dij_dist_dict_command,
    graph_protocols.COMMAND_DIJKISTRA_PREV_DICT: graph_protocols.execute_dij_prev_dict_command,
    graph_protocols.COMMAND_DIJKISTRA_SHORTEST_PATH: graph_protocols.execute_dij_shortest_path_command,
}
