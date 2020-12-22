from pymongo import MongoClient
 
connection = MongoClient()
db = connection.users_information

def new_user(chat_id, alias):
    """Function to add new user to database

    Args:
        chat_id (string): id of new user in telegram
        alias (string): alias of new user
    """
    user_info = {'_id': chat_id,
                 'next_published_offer_id': 0, 
                 'next_taken_offer_id': 0,
                 'alias': alias,
                 'published_offers': {},
                 'taken_offers': {},
                 'profile': {'published_offers': 0, 
                             'taken_offers': 0,
                             'in_kazan': 0,
                             'rating': 0,
                             'rating_count': 0,
                             },
                 }

    user_id = db.users.insert_one(user_info).inserted_id


def change_profile(chat_id):
    user = db.users.find_one({'_id': chat_id})
    if 'your_offers' in user['profile']:
        user['profile'] = {'published_offers': 0,
                           'taken_offers': 0,
                           'in_kazan': 0,
                           'rating': 0,
                           'rating_count': 0,
                        }
    db.users.save(user)


def get_profile_num(chat_id):
    user = db.users.find_one({'_id': chat_id})
    profile = user['profile']
    return [profile['published_offers'], profile['taken_offers'], profile['in_kazan']]


def kazan_status(chat_id, status):
    user = db.users.find_one({'_id': chat_id})
    user['profile']['in_kazan'] = status
    db.users.save(user)

    
def user_exists(chat_id):
    """Check that field of user exists in database

    Args:
        chat_id (string): id of user in telegram
    """
    return db.users.find_one({'_id':chat_id}) != None


def add_dungling_offer(chat_id, shop, item, bounty):
    user = db.users.find_one({'_id': chat_id})
    user['dungling_offer'] = {'shop': shop, 'item': item, 'bounty': bounty}
    db.users.save(user)


def approve_offer(chat_id):
    """Move offer from dungling to list of all offers if user will approve it.

    Args:
        chat_id (string): id of user in Telegram
    """
    user = db.users.find_one({'_id': chat_id})
    # dungling offer
    dung_offer = user['dungling_offer']
    adding_index = user['next_published_offer_id']
    user['published_offers'][str(adding_index)] = dung_offer
    # update the id for next offer
    user['next_published_offer_id'] += 1
    db.users.save(user)
    return dung_offer


def list_published_offers(chat_id):
    """Function that return list of dicts of user published offers

    Args:
        chat_id (int): id of user

    Returns:
        list: list of user's published offers
    """
    user = db.users.find_one({'_id': chat_id})
    return user['published_offers']


def list_taken_offers(chat_id):
    """Function that return list of dicts of user taken offers from DB

    Args:
        chat_id (int): id of user

    Returns:
        list: list of user's published offers
    """
    user = db.users.find_one({'_id': chat_id})
    return user['taken_offers']


def list_all_offers(chat_id):
    """Function that returns information about users except the one who send a request

    Args:
        chat_id (int): id of user in telegram and DB that send request

    Returns:
        dict: information about all users
    """
    all_users = db.users.find({'_id': {'$nin': [chat_id]}})
    return all_users

def list_users_in_kazan(chat_id):
    kazan_users = db.users.find({'_id': {'$nin': [chat_id]}, 'profile': {'in_kazan': 1}})
    return kazan_users


def delete_published_offer(chat_id, offer_id):
    """Function to delete published offer from user db document 

    Args:
        chat_id (int): id of user in telegram and in DB
        offer_id (string): id of offer that we need to delete
    """
    user = db.users.find_one({'_id': chat_id})
    print('offer deleted')
    print(user['published_offers'][offer_id])
    del user['published_offers'][offer_id]
    db.users.save(user)


def delete_taken_offer(chat_id, offer_id):
    """Function to delete taken offer from user db document 

    Args:
        chat_id (int): id of user in telegram and in DB
        offer_id (string): id of offer that we need to delete
    """
    user = db.users.find_one({'_id': chat_id})
    print('offer deleted')
    print(user['taken_offers'][offer_id])
    del user['taken_offers'][offer_id]
    db.users.save(user)
    
    
def take_offer(chat_id, user_id, number):
    """Function to accepting offer of one user by another

    Args:
        chat_id (int): id of user that take offer
        user_id (int): id of user that published offer
        number (string): number of offer in published offer list of reciever in DB
    """
    taker = db.users.find_one({'_id': chat_id})
    reciever = db.users.find_one({'_id': user_id})
    
    taken_offers_adding_index = taker['next_taken_offer_id']
    offer = reciever['published_offers'][number]
    offer['alias'] = taker['alias']
    
    # different offer variable because we need to write
    # different aliases fot taker and reciever
    taken_offer = offer
    taken_offer['alias'] = reciever['alias']
    taker['taken_offers'][str(taken_offers_adding_index)] = taken_offer
    
    taker['next_taken_offer_id'] += 1
    
    taker_alias = taker['alias']
    reciever['published_offers'][number]['taker_alias'] = taker_alias
    reciever['taken_offers']['taken'+number] = reciever['published_offers'][number] 

    del reciever['published_offers'][number]
    
    db.users.save(taker)
    db.users.save(reciever)


def get_alias(chat_id):
    """Returns alias of user by its id in DB

    Args:
        chat_id (int): id of user alias of which we want

    Returns:
        string: alias of user from DB
    """
    return db.users.find_one({'_id': chat_id})['alias']