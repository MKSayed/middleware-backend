from fastapi import HTTPException

from models.models_connector import ModuleParameter
from models.models_service import ServiceParameter


class ParameterNode:
    def __init__(self, id: int, key: str, value_reference_id: int | None, value=None, parent_ser: int = None, is_optional: bool = False):
        self.id = id
        self.key = key
        self.value_reference_id = value_reference_id
        self.value = value
        self.parent_ser = parent_ser
        self.is_optional = is_optional
        self.children: list[ParameterNode] = []


def build_parameter_tree(parameters: list[ServiceParameter]) -> dict[int, ParameterNode]:
    """Build a tree structure of parameters."""
    nodes = {param.id: ParameterNode(param.id, param.key, param.value_reference_id, param.value, param.parent_id, param.is_optional) for param in parameters}
    root_nodes = {}
    for param in parameters:
        # param.parent_id can be referencing either ServiceParameter.id or ModuleParameter.id
        if param.parent_id:
            nodes[param.parent_id].children.append(nodes[param.id])
        else:
            root_nodes[param.id] = nodes[param.id]
    return root_nodes


async def attach_ids_and_values(db, data: dict, node: ParameterNode, result: dict,
                                       global_session_data_collection: dict[str, list] | None = None):
    """Recursively attach dataIdentifiers to the data."""
    if node.key in data:
        value = data[node.key]
        if isinstance(value, dict):
            new_value = {}
            for child in node.children:
                await attach_ids_and_values(db, value, child, new_value, global_session_data_collection)
            result[node.key] = new_value
        else:
            # check if the stored value is a dict. which means client is going to send the dict key and we use it's value
            if isinstance(eval(str(node.value)), dict):
                if value not in node.value:
                    raise HTTPException(status_code=400, detail=f'The key {value} sent by the client doesn\'t exist in the saved value {node.value} the parameter {node.key}')
                result[node.key] = {node.id, node.value[value]}
            result[node.key] = (node.id, value)
    elif node.value:
        result[node.key] = (node.id, node.value)
    elif node.value_reference_id and global_session_data_collection:
        # This logic is needed to handle the case where the data is not provided in the request body but is
        # available in the global session data collection from previous session's requests' responses.
        flag_complete = False
        for item in global_session_data_collection:
            #  bigger than 3000 means it's a service parameter
            if node.value_reference_id >= 3000:
                current_param = await ServiceParameter.find(db, id=node.value_reference_id)
            #  smaller than 3000 means it's a service parameter
            else:
                current_param = await ModuleParameter.find(db, id=node.value_reference_id)
            data_list = find_all(item, current_param.key)
            if not data_list:
                continue
            else:
                for data_element in data_list:
                    if data_element[current_param.key][0] == node.value_reference_id:
                        result[node.key] = (node.id, data_element[current_param.key][1])
                        flag_complete = True
                        break
        if not flag_complete and not node.is_optional:
            raise HTTPException(status_code=400,
                                detail=f"Data for key '{node.key}' not found in the provided data nor in global session data collection")
    elif not node.is_optional:
        raise HTTPException(status_code=400,
                            detail=f"Data for key '{node.key}' not found in the provided data nor in global session data collection")


def find_all(d, key):
    """
    Recursively searches for all dictionaries within the nested dictionary 'd' that contain the specified 'key'.
    Returns a list of dictionaries containing the key.
    """
    if not isinstance(d, dict):
        return []

    found = []
    if key in d:
        found.append(d)

    for k, v in d.items():
        if isinstance(v, dict):
            found.extend(find_all(v, key))
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    found.extend(find_all(item, key))

    return found


def replace_tuples(data):
    if isinstance(data, dict):
        # Recursively apply to all dictionary values
        return {key: replace_tuples(value) for key, value in data.items()}
    elif isinstance(data, list):
        # Recursively apply to all list elements
        return [replace_tuples(element) for element in data]
    elif isinstance(data, tuple):
        # Replace tuple with tuple[1]
        return data[1] if len(data) > 1 else print('Error in replace_tuples: Tuple has no second element')
    else:
        # Return the data as is if it's not a dict, list, or tuple
        return data
