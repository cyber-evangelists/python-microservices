import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc
from model import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re
engine = create_engine('sqlite:///users.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def CreateUser(self, request, context):
        session = self.Session()
        try:
            # Validate name and email
            name = request.name.strip() if request.name else None
            email = request.email.strip() if request.email else None
            
            if not name:
                return user_pb2.CreateUserResponse(message='Name is required')
            if not email:
                return user_pb2.CreateUserResponse(message='Email is required')
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return user_pb2.CreateUserResponse(message='Invalid email format')

            # Create and add user to the database
            new_user = User(name=name, email=email)
            session.add(new_user)
            session.commit()
            return user_pb2.CreateUserResponse(message='User created successfully')
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def GetAllUsers(self, request, context):
        session = self.Session()
        try:
            users = session.query(User).all()
            serialized_users = [user_pb2.User(id=user.id, name=user.name, email=user.email) for user in users]
            return user_pb2.GetAllUsersResponse(users=serialized_users)
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def GetUser(self, request, context):
        session = self.Session()
        try:
            if not request.user_id:
                return user_pb2.UpdateUserResponse(message=f"User ID is required")
            uid = request.user_id
          
            
            user = session.query(User).filter_by(id=uid).first()
            print(user)
            if user is not None:
                serialized_user = user_pb2.User(id=user.id, name=user.name, email=user.email)
                return user_pb2.GetUserResponse(user=serialized_user)
            else:
              
             
                return user_pb2.GetUserResponse(message=f"User with ID {uid} not found")
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()
    def UpdateUser(self, request, context):
        session = self.Session()
        try:
            uid = request.user_id
            new_name = request.name.strip() if request.name else None
            new_email = request.email.strip() if request.email else None

            if not new_name:
                return user_pb2.UpdateUserResponse(message='Name is required')
            if not new_email:
                return user_pb2.UpdateUserResponse(message='Email is required')
            if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
                return user_pb2.UpdateUserResponse(message='Invalid email format')

            user = session.query(User).filter_by(id=uid).first()
            if user:
                user.name = new_name
                user.email = new_email
                session.commit()
                return user_pb2.UpdateUserResponse(message=f"User with ID {uid} updated successfully")
            else:
                return user_pb2.UpdateUserResponse(message=f"User with ID {uid} not found")
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()
    def DeleteUser(self, request, context):
        session = self.Session()
        try:
            if not user_id:
                return user_pb2.UpdateUserResponse(message=f"User ID is required")
            user_id = request.user_id
        
            
        
            user = session.query(User).filter_by(id=user_id).first()
            if user:
              
                session.delete(user)
                session.commit()
                return user_pb2.DeleteUserResponse(message=f"User with ID {user_id} deleted successfully")
            else:
             
                return user_pb2.DeleteUserResponse(message=f"User with ID {user_id} not found")
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()


            
            

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
