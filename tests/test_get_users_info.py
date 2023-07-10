from modules.functions.get_users_info import get_user_id, get_user_login, get_user_name


def test_get_correct_user_id():
    user_id = get_user_id('admin')

    assert user_id == 9

def test_get_incorrect_user_id():
    user_id = get_user_id('testadmin')

    assert user_id == False

def test_get_correct_user_login():
    login = get_user_login(9)[0]

    assert login == 'admin'

def test_get_incorrect_user_login():
    login = get_user_login(150)

    assert login == False

def test_get_correct_user_name():
    user = get_user_name('admin')
    user_id = user[0]
    user_name = user[1]

    assert user_id == 9
    assert user_name == 'Anon'

def test_get_incorrect_user_name():
    user = get_user_name('testadmin')

    assert user == False