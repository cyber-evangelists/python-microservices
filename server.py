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
from auth.auth_handler import signJWT,decodeJWT
import jwt


class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.Session = sessionmaker(bind=engine)
    
    
    def LoginUser(self, request, context):
        session = self.Session()
        try:
        
            req_name = request.name.strip() if request.name else None
            req_email = request.email.strip() if request.email else None
          

            if not req_name:
                return user_pb2.LoginUserResponse(message='Email is required')
            if not req_email:
                return user_pb2.LoginUserResponse(message='Password is required')

            # Query the database to check if the user exists with the provided email and password
            user = session.query(User).filter_by(name=req_name, email=req_email).first()
        
            if user:  
                token = signJWT(req_name)
                return user_pb2.LoginUserResponse(token=token, message='Login successful')
            else:
                return user_pb2.LoginUserResponse(message='Invalid email or password')
        except Exception as e:
            session.rollback()
            return user_pb2.LoginUserResponse(message='User Login unsucessful')
        finally:
            session.close()

    def CreateUser(self, request, context):
        session = self.Session()
        try:
            metadata = dict(context.invocation_metadata())
            token = metadata.get('authorization')
            
            if token:
                try:
                    decoded_token, is_expired = decodeJWT(token)
                    if decoded_token:
                        name = request.name.strip() if request.name else None
                        email = request.email.strip() if request.email else None

                        if not name:
                            return user_pb2.CreateUserResponse(message='Name is required')
                        if not email:
                            return user_pb2.CreateUserResponse(message='Email is required')
                        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                            return user_pb2.CreateUserResponse(message='Invalid email format')

                        new_user = User(name=name, email=email)
                        session.add(new_user)
                        session.commit()
                        return user_pb2.CreateUserResponse(message='User created successfully')
                    elif is_expired:
                        return user_pb2.CreateUserResponse(message='Expired JWT token')
                    else:
                        return user_pb2.CreateUserResponse(message='Invalid JWT token')
                except jwt.InvalidTokenError:
                    return user_pb2.CreateUserResponse(message='Invalid JWT token')
            else:
                return user_pb2.CreateUserResponse(message='JWT token missing')
        except Exception as e:
            session.rollback()
            return user_pb2.CreateUserResponse(message='User creation unsuccessful')
        finally:
            session.close()

    def GetAllUsers(self, request, context):
        session = self.Session()
        metadata = dict(context.invocation_metadata())
        token = metadata.get('authorization')
        if token:
            try:
                decoded_token, is_expired = decodeJWT(token)
                if decoded_token:
                    users = session.query(User).all()
                    serialized_users = [user_pb2.User(id=user.id, name=user.name, email=user.email) for user in users]
                    return user_pb2.GetAllUsersResponse(users=serialized_users)
                else:
                    return user_pb2.GetAllUsersResponse(message="Invalid or expired jwt")
            except Exception as e:
                session.rollback()
                return user_pb2.GetAllUsersResponse(message='Users cannot be retrieved')
            finally:
                session.close()

    def GetUser(self, request, context):
        session = self.Session()
        metadata = dict(context.invocation_metadata())
        token = metadata.get('authorization')
        if token:
            try:
                decoded_token, is_expired = decodeJWT(token)
                if decoded_token:
                    if not request.user_id:
                        return user_pb2.GetUserResponse(message=f"User ID is required")
                    uid = request.user_id
                
                    
                    user = session.query(User).filter_by(id=uid).first()
                    if user is not None:
                        serialized_user = user_pb2.User(id=user.id, name=user.name, email=user.email)
                        return user_pb2.GetUserResponse(user=serialized_user)
                    else:
                    
                    
                        return user_pb2.GetUserResponse(message=f"User with ID {uid} not found")
                else:
                     return user_pb2.GetUserResponse(message=f"Invalid or expired JWT")
            except Exception as e:
                session.rollback()
                return user_pb2.GetUserResponse(message='User could not be found')
            finally:
                session.close()
    
    def UpdateUser(self, request, context):
        session = self.Session()
        metadata = dict(context.invocation_metadata())
        token = metadata.get('authorization')
        if token:
            try:
                decoded_token, is_expired = decodeJWT(token)
                if decoded_token:
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
                else:
                     return user_pb2.UpdateUserResponse(message=f"Invalid or Expired JWT")
            except Exception as e:
                session.rollback()
                return user_pb2.UpdateUserResponse(message='User could not be updated')
            finally:
                session.close()
    def DeleteUser(self, request, context):
        session = self.Session()
        metadata = dict(context.invocation_metadata())
        token = metadata.get('authorization')
        if token:
            try:
                decoded_token, is_expired = decodeJWT(token)
                if decoded_token:
                    if not request.user_id:
                        return user_pb2.UpdateUserResponse(message=f"User ID is required")
                    user_id = request.user_id
                    print(user_id)
                
                    
                
                    user = session.query(User).filter_by(id=user_id).first()
                    if user:
                    
                        session.delete(user)
                        session.commit()
                        return user_pb2.DeleteUserResponse(message=f"User with ID {user_id} deleted successfully")
                    else:
                    
                        return user_pb2.DeleteUserResponse(message=f"User with ID {user_id} not found")
                else:  
                    return user_pb2.DeleteUserResponse(message=f"Invalid or expired jwt")
            except Exception as e:
                session.rollback()
                return user_pb2.DeleteUserResponse(message='User could not be deleted')
            finally:
                session.close()


            
            

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is active")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
