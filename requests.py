import grpc
import user_pb2
import user_pb2_grpc

def InsertUser():
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)
    response = stub.CreateUser(user_pb2.CreateUserRequest(name='John', email='john@example.com'))
    print(response.message)
def GetAllUser():
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)
    
    try:
     
        request = user_pb2.Empty()

      
        response = stub.GetAllUsers(request)

       
        for user in response.users:
            print(f"User ID: {user.id}, Name: {user.name}, Email: {user.email}")
    except grpc.RpcError as e:
        print(f"Error occurred: {e.details()}")
def GetUserByID(user_id):
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)
    
    try:
        request = user_pb2.GetUserRequest(user_id=user_id)
        response = stub.GetUser(request)
        if response.user:
            print(f"User ID: {response.user.id}, Name: {response.user.name}, Email: {response.user.email}")
        else:
            print(response.message) 
    except grpc.RpcError as e:
         print(f"Error occurred: {e}")
def UpdateUserByID(user_id, new_name, new_email):
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)
    
    try:
      
        request = user_pb2.UpdateUserRequest(user_id=user_id, name=new_name, email=new_email)

     
        response = stub.UpdateUser(request)

      
        print(response.message)
    except grpc.RpcError as e:
        print(f"Error occurred: {e.details()}")
        
def DeleteUserByID(user_id):
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)
    
    try:
       
        request = user_pb2.DeleteUserRequest(user_id=user_id)

     
        response = stub.DeleteUser(request)

       
        print(response.message)
    except grpc.RpcError as e:
        print(f"Error occurred: {e.details()}")





if __name__ == '__main__':
    # InsertUser()
    # GetAllUser()
    GetUserByID(1)
    # UpdateUserByID(user_id=2, new_name="New Name", new_email="newemail@example.com")
    # DeleteUserByID(user_id=3)
    
