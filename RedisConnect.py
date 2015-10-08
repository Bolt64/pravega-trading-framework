from logic import Problem, UserLogic, Commodity
from RedisLocks import RedisWriteLock
import redis

def get_user_from_redis(user, connection_pool):
    connection = redis.Redis(connection_pool=connection_pool)
    with RedisWriteLock(connection, user, 0.01, 2):
        try:
            result = UserLogic.fromString(connection.get(user).decode())
            return result
        except AttributeError:
            return None

def get_problem_from_redis(problem_id, problem_pool):
    connection = redis.Redis(connection_pool=problem_pool)
    with RedisWriteLock(connection, problem_id, 0.01, 2):
        result = Problem.fromString(connection.get(problem_id).decode())
        return result
