import grpc
import user_pb2
import user_pb2_grpc
def LoginUser(name, email):
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)
    try:
        request = user_pb2.LoginUserRequest(name=name, email=email)
        response = stub.LoginUser(request)
        if response.token:
            print(f"Login successful",response.token)
        else:
            print(response.message) 
    except grpc.RpcError as e:
         print(f"Error occurred: {e}")


def InsertUser():
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)
    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiVGVzdCIsImV4cGlyZXMiOjE3MTU5NjA1MzkuNTcxNDIyfQ.pGBmI1RK0pXbgFiGnJnx7QS3LGg5Z7iiBnU6JmOwns8"
    metadata = [('authorization', f'Bearer {jwt_token}')]
    request = user_pb2.CreateUserRequest(name='User23', email='user23@example.com')
    response = stub.CreateUser(request, metadata=metadata)
    print(response)

   
    
def GetAllUser():
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)
    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiVGVzdCIsImV4cGlyZXMiOjE3MTUyNTUyODUuNjg5MjQ1fQ.X1SCn6BGFflBb37vElDPJV1fs2-2xpH5KsHzxgmZRNo"
    
    # Set JWT token in the request metadata
    metadata = [('authorization', f'Bearer {jwt_token}')]
    
    try:
        request = user_pb2.Empty()
        # Pass metadata with the request
        response = stub.GetAllUsers(request, metadata=metadata)
        for user in response.users:
            print(f"User ID: {user.id}, Name: {user.name}, Email: {user.email}")
    except grpc.RpcError as e:
        print(f"Error occurred: {e.details()}")

def GetUserByID(user_id):
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)
    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiVGVzdCIsImV4cGlyZXMiOjE3MTUyNTUyODUuNjg5MjQ1fQ.X1SCn6BGFflBb37vElDPJV1fs2-2xpH5KsHzxgmZRNo"
    
    # Set JWT token in the request metadata
    metadata = [('authorization', f'Bearer {jwt_token}')]
    try:
        request = user_pb2.GetUserRequest(user_id=user_id)
        response = stub.GetUser(request,metadata=metadata)
        if response.user:
            print(f"User ID: {response.user.id}, Name: {response.user.name}, Email: {response.user.email}")
        else:
            print(response.message) 
    except grpc.RpcError as e:
         print(f"Error occurred: {e}")
def UpdateUserByID(user_id, new_name, new_email):
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)
    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiVGVzdCIsImV4cGlyZXMiOjE3MTUyNTUyODUuNjg5MjQ1fQ.X1SCn6BGFflBb37vElDPJV1fs2-2xpH5KsHzxgmZRNo"
    
    # Set JWT token in the request metadata
    metadata = [('authorization', f'Bearer {jwt_token}')]
    
    try:
        request = user_pb2.UpdateUserRequest(user_id=user_id, name=new_name, email=new_email)
        response = stub.UpdateUser(request,metadata=metadata)
        print(response.message)
    except grpc.RpcError as e:
        print(f"Error occurred: {e.details()}")
def DeleteUserByID(user_id):
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)
    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiVGVzdCIsImV4cGlyZXMiOjE3MTUyNTUyODUuNjg5MjQ1fQ.X1SCn6BGFflBb37vElDPJV1fs2-2xpH5KsHzxgmZRNo"
 
   
    metadata = [('authorization', f'Bearer {jwt_token}')]
    
    try:
        request = user_pb2.DeleteUserRequest(user_id=user_id)  
        response = stub.DeleteUser(request,metadata=metadata)
        print(response.message)
    except grpc.RpcError as e:
        print(f"Error occurred: {e.details()}")

if __name__ == '__main__':
    InsertUser()
    # GetAllUser()
    # GetUserByID(12)
    # LoginUser(name="Test", email="test@example.com")
    # UpdateUserByID(user_id=20, new_name="New Name", new_email="newemail@example.com")
    # DeleteUserByID(user_id=13)
