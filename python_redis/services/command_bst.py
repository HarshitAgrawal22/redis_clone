import python_redis.protocols.bst_protocols as bst_protocols
import python_redis.execution.Dispatchers.dispatch_tree as bst_dispatchers
import python_redis.execution.tree_exe as bst_executer
import python_redis.commands.tree as cmds

execute_task_bst = {
    bst_protocols.SetKeyCommand: bst_dispatchers.TREE_TASKS.task_set_key_command,
    bst_protocols.DeleteCommand: bst_dispatchers.TREE_TASKS.task_delete_command,
    bst_protocols.DisplayCommand: bst_dispatchers.TREE_TASKS.task_display_command,
    bst_protocols.SearchCommand: bst_dispatchers.TREE_TASKS.task_search_node_command,
    bst_protocols.InOrderTraversalCommand: bst_dispatchers.TREE_TASKS.task_in_order_traversal_command,
    bst_protocols.PreOrderTraversalCommand: bst_dispatchers.TREE_TASKS.task_pre_order_traversal_command,
    bst_protocols.PostOrderTraversalCommand: bst_dispatchers.TREE_TASKS.task_post_order_traversal_command,
    bst_protocols.InsertCommand: bst_dispatchers.TREE_TASKS.task_insert_command,
    bst_protocols.GetKeyCommand: bst_dispatchers.TREE_TASKS.task_get_key_command,
    bst_protocols.UpsertCommand: bst_dispatchers.TREE_TASKS.task_upsert_node_values,
}
execute_command_bst = {
    cmds.COMMAND_UPSERT_NODE_KEY_VAL: bst_executer.execute_upsert_key_val_command,
    cmds.COMMAND_DELETE: bst_executer.execute_delete_command,
    cmds.COMMAND_IN_ORDER: bst_executer.execute_in_order_traversal_command,
    cmds.COMMAND_GET: bst_executer.execute_get_command,
    cmds.COMMAND_INSERT: bst_executer.execute_insert_command,
    cmds.COMMAND_SEARCH: bst_executer.execute_search_command,
    cmds.COMMAND_POST_ORDER: bst_executer.execute_post_order_traversal_command,
    cmds.COMMAND_PRE_ORDER: bst_executer.execute_pre_order_traversal_command,
    cmds.COMMAND_SHOW: bst_executer.execute_display_command,
    cmds.COMMAND_SET: bst_executer.execute_set_command,
}
