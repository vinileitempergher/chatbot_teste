user_states = {}

def get_user_state(user_phone):
    return user_states.get(user_phone, 'menu')

def set_user_state(user_phone, state):
    user_states[user_phone] = state