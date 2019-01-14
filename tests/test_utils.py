from sspider.utils.user_agents import replace_user_agent


def test_agent():
    headers = {'headers': {}}
    replace_user_agent(headers)
    assert 'user-agent' in headers['headers']
