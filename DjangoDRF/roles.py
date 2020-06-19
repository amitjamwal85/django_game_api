from rolepermissions.roles import AbstractUserRole


class Administrator(AbstractUserRole):
    available_permissions = {
        'all_permission': True,
    }


class Assistant(AbstractUserRole):
    available_permissions = {
        'read_data': True,
        'post_data': True,
        'delete_data': True,
        'update_data': True
    }