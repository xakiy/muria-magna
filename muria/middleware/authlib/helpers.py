def query_client(client_id):
    raise NotImplementedError()
    # return Client.query.filter_by(client_id=client_id).first()

def save_token(token, request):
    raise NotImplementedError()
    # if request.user:
    #     user_id = request.user.get_user_id()
    # else:
    #     # client_credentials grant_type
    #     user_id = request.client.user_id
    #     # or, depending on how you treat client_credentials
    #     user_id = None
    # item = Token(
    #     client_id=request.client.client_id,
    #     user_id=user_id,
    #     **token
    # )
    # db.session.add(item)
    # db.session.commit()
