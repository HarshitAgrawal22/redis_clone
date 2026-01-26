import python_redis.protocols.graph_protocols as graph_protocols
import python_redis.commands.granph as cmds
import python_redis.execution.Dispatchers.dispatch_graph as graph_dispatchers
import python_redis.execution.graph_exe as graph_executer

execute_task_graph = {
    graph_protocols.AddEdgeCommand: graph_dispatchers.GRAPH_TASKS.task_add_edge_command,
    graph_protocols.AddVertexCommand: graph_dispatchers.GRAPH_TASKS.task_add_vertex_command,
    graph_protocols.RemoveEdgeCommand: graph_dispatchers.GRAPH_TASKS.task_remove_edge_command,
    graph_protocols.RemoveVertexCommand: graph_dispatchers.GRAPH_TASKS.task_remove_vertex_command,
    graph_protocols.BFSCommand: graph_dispatchers.GRAPH_TASKS.task_bfs_command,
    graph_protocols.DFSCommand: graph_dispatchers.GRAPH_TASKS.task_dfs_command,
    graph_protocols.IsDirectedCommand: graph_dispatchers.GRAPH_TASKS.task_is_directed_command,
    graph_protocols.IsWeightedCommand: graph_dispatchers.GRAPH_TASKS.task_is_weighted_command,
    graph_protocols.DisplayCommand: graph_dispatchers.GRAPH_TASKS.task_display_command,
    graph_protocols.GetVertexCommand: graph_dispatchers.GRAPH_TASKS.task_get_vertex_by_value_command,
    graph_protocols.GetVerticesCommand: graph_dispatchers.GRAPH_TASKS.task_get_vertices_command,
    graph_protocols.GetEdgesByVertexCommand: graph_dispatchers.GRAPH_TASKS.task_get_edges_by_vertex_command,
    graph_protocols.GetKeyCommand: graph_dispatchers.GRAPH_TASKS.task_get_key_command,
    graph_protocols.SetKeyCommand: graph_dispatchers.GRAPH_TASKS.task_set_key_command,
    graph_protocols.DijkistraDistDictionaryCommand: graph_dispatchers.GRAPH_TASKS.task_dijkistra_dist_dict_command,
    graph_protocols.DijkistraPrevDictionaryCommand: graph_dispatchers.GRAPH_TASKS.task_dijkistra_prev_dict_command,
    graph_protocols.DijkistraShortestPathCommand: graph_dispatchers.GRAPH_TASKS.task_dijkistra_shortest_path_command,
}
execute_command_graph = {
    cmds.COMMAND_SET_KEY: graph_executer.execute_set_key_command,
    cmds.COMMAND_GET_KEY: graph_executer.execute_get_key_command,
    cmds.COMMAND_BFS: graph_executer.execute_breadth_first_search_command,
    cmds.COMMAND_DFS: graph_executer.execute_depth_first_search_command,
    cmds.COMMAND_ADD_VERTEX: graph_executer.execute_add_vertex_command,
    cmds.COMMAND_ADD_EDGE: graph_executer.execute_add_edge_command,
    cmds.COMMAND_REMOVE_VERTEX: graph_executer.execute_remove_vertex_by_value_command,
    cmds.COMMAND_REMOVE_EDGE: graph_executer.execute_remove_edge_command,
    cmds.COMMAND_IS_WEIGHTED: graph_executer.execute_is_weighted_command,
    cmds.COMMAND_IS_DIRECTED: graph_executer.execute_is_directed_command,
    cmds.COMMAND_SHOW: graph_executer.execute_display_command,
    cmds.COMMAND_GET_VERTEX_BY_VALUE: graph_executer.execute_get_vertex_by_value_command,
    cmds.COMMAND_GET_VERTICES: graph_executer.execute_get_vertices_command,
    cmds.COMMAND_GET_VERTEX_EDGE: graph_executer.execute_get_edges_by_vertex_command,
    cmds.COMMAND_DIJKISTRA_DIST_DICT: graph_executer.execute_dij_dist_dict_command,
    cmds.COMMAND_DIJKISTRA_PREV_DICT: graph_executer.execute_dij_prev_dict_command,
    cmds.COMMAND_DIJKISTRA_SHORTEST_PATH: graph_executer.execute_dij_shortest_path_command,
}
