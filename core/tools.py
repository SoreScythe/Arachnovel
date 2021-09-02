from random import choice

user_agents = [ua.strip() for ua in open('user_agents.txt', 'r').readlines()]
proxies = [proxy.strip() for proxy in open('proxies.txt', 'r').readlines()]

def random_proxy():
    return choice(proxies)

def random_ua():
    return choice(user_agents).strip()