from etl.extract.data_extraction import fetch_random_user

def load_users_to_system(limit: int):
    users_list = []
    """  
    Retrieves a list of users according to the limit length
    """
    while len(users_list) < limit:
        new_user = fetch_random_user()
        if new_user not in users_list:
            users_list.append(new_user)
        print("user added")
    return users_list