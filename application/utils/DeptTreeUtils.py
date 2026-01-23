def parse_dept_tree(dept_list):
    # 创建字典用于快速查找部门，以部门ID为键
    dept_dict = {}
    for dept in dept_list:
        dept_dict[dept.id] = {
            'id': dept.id,
            'name': dept.name,
            'parentId': dept.parentId,
            'level': dept.level,
            'fullParentId': dept.fullParentId,
            'fullParentName': dept.fullParentName,
            'children': []
        }

    # 创建结果列表，用于存放根节点
    result = []

    # 遍历所有部门，构建树形结构
    for dept in dept_list:
        dept_node = dept_dict[dept.id]

        # 如果父ID为0或None，表示是根节点
        if dept.parentId == 0 or dept.parentId is None:
            result.append(dept_node)
        else:
            # 查找父节点，如果存在则将当前节点添加到父节点的children中
            parent_node = dept_dict.get(dept.parentId)
            if parent_node:
                parent_node['children'].append(dept_node)

    return result

