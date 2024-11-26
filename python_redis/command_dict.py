import keyval_protocol


execute_task_hash_map: dict = {
    keyval_protocol.SetCommand: keyval_protocol.HASHMAP_TASKS.task_set_command,
    keyval_protocol.GetCommand: keyval_protocol.HASHMAP_TASKS.task_get_command,
    keyval_protocol.ClientCommand: keyval_protocol.HASHMAP_TASKS.task_client_command,
    keyval_protocol.DeleteCommand: keyval_protocol.HASHMAP_TASKS.task_delete_command,
    keyval_protocol.HelloCommand: keyval_protocol.HASHMAP_TASKS.task_hello_command,
    keyval_protocol.QuitCommand: keyval_protocol.HASHMAP_TASKS.task_quit_command,
    keyval_protocol.CheckCommand: keyval_protocol.HASHMAP_TASKS.task_check_command,
    keyval_protocol.GetMultipleAttributeCommand: keyval_protocol.HASHMAP_TASKS.task_get_multiple_attrs_command,
    keyval_protocol.TotalCommand: keyval_protocol.HASHMAP_TASKS.task_total_command,
    keyval_protocol.GetMultipleKeyValCommand: keyval_protocol.HASHMAP_TASKS.task_get_multi_key_val_command,
    keyval_protocol.SetMultipleAttributeCommand: keyval_protocol.HASHMAP_TASKS.task_set_multiple_attrs_command,
    keyval_protocol.SetMultipleKeyValCommand: keyval_protocol.HASHMAP_TASKS.task_set_multi_key_val_command,
    keyval_protocol.IncrementCommand: keyval_protocol.HASHMAP_TASKS.task_increment_command,
}

execute_command_hash_map: dict = {
    keyval_protocol.COMMAND_SET: keyval_protocol.execute_set_command,
    keyval_protocol.COMMAND_DELETE: keyval_protocol.execute_delete_command,
    keyval_protocol.COMMAND_CHECK: keyval_protocol.execute_check_command,
    keyval_protocol.COMMAND_CLIENT: keyval_protocol.execute_client_command,
    keyval_protocol.COMMAND_GET: keyval_protocol.execute_get_command,
    keyval_protocol.COMMAND_QUIT: keyval_protocol.execute_quit_command,
    keyval_protocol.COMMAND_GET_MULTIPLE_VALUES: keyval_protocol.execute_get_multiple_values_command,
    keyval_protocol.COMMAND_INCREMENT: keyval_protocol.execute_incry_command,
    keyval_protocol.COMMAND_TOTAL: keyval_protocol.execute_total_command,
    keyval_protocol.COMMAND_MULTIPLE_ATTRIBUTE_GET: keyval_protocol.execute_multiple_attrs_get_command,
    keyval_protocol.COMMAND_MULTIPLE_ATTRIBUTE_SET: keyval_protocol.execute_multiple_attrs_set_command,
    keyval_protocol.COMMAND_SET_MULTIPLE_KEY_VAL: keyval_protocol.execute_set_multi_key_val_command,
    keyval_protocol.COMMAND_HELLO: keyval_protocol.execute_hello_command,
}

execute_command_queue: dict = {}
