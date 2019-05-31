from modules.ProfileManager.api.db_methods import db_getProfileInfo


def isProfileBlocked(user_id):
    return db_getProfileInfo(user_id)['is_blocked']


def isProfileDeleted(user_id):
    return db_getProfileInfo(user_id)['is_deleted']