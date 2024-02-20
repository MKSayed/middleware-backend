# from models.models_user import User
# from schemas.schemas_user.user_schema import UserBase
# from sqlalchemy.orm import Session
#
#
# def create_user(request: UserBase, db: Session):
#     new_user = User(
#         id = request.id,
#         name=request.name,
#         national_id=request.national_id,
#         tax_id=request.tax_id,
#         fk_user_typecd=request.fk_user_typecd,
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
#
# def get_all_users(db: Session):
#     return db.query(User).all()
#
# def get_user(db: Session, id: int):
#     return db.query(User).filter(User.id == id).first()