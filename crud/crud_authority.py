from crud import CRUDBase
from models import Application, TransactionKiosk, Authority, AuthorizedRole, AssignedRole


class CRUDApplication(CRUDBase):
    pass


crud_application = CRUDApplication(Application)


class CRUDTransactionKiosk(CRUDBase):
    pass


crud_transaction_kiosk = CRUDTransactionKiosk(TransactionKiosk)


class CRUDAuthority(CRUDBase):
    pass


crud_authority = CRUDAuthority(Authority)


class CRUDAuthorizedRole(CRUDBase):
    pass


crud_authorized_role = CRUDAuthorizedRole(AuthorizedRole)


class CRUDAssignedRole(CRUDBase):
    pass


crud_assigned_role = CRUDAssignedRole(AssignedRole)
