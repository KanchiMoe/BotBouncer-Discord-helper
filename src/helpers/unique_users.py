import logging

def get_unique_users_post_pushshift(json_data):
    users = set()

    # for each item in json_data
    # get "author"
    # if "user" is not empty
    # add to set
    for item in json_data:
        user = item.get("author")
        if user:
            users.add(user)

    logging.info("Extracted %s unique users", len(users))
    return users
