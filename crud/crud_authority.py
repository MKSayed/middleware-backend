from crud import CRUDBase
from models.models_authority import Application, Permission, Authority, AuthorizedRole, AssignedRole


class CRUDApplication(CRUDBase):
    pass


crud_application = CRUDApplication(Application)


class CRUDTransactionKiosk(CRUDBase):
    pass


crud_transaction_kiosk = CRUDTransactionKiosk(Permission)


class CRUDAuthority(CRUDBase):
    pass


crud_authority = CRUDAuthority(Authority)


class CRUDAuthorizedRole(CRUDBase):
    pass


crud_authorized_role = CRUDAuthorizedRole(AuthorizedRole)


class CRUDAssignedRole(CRUDBase):
    pass


crud_assigned_role = CRUDAssignedRole(AssignedRole)
