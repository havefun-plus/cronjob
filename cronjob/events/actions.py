class Action:
    def __init__(self, name):
        self.name = name


pre_action = Action('pre_action')
post_action = Action('post_action')
err_action = Action('err_action')
