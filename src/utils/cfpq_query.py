from redis import Redis

COMMON_CMD = 'graph.cfg'


def _get_time(resp):
    return float(resp[0].split()[-1])


def _get_rss(resp):
    return int(resp[1].split()[-1])


def _get_vms(resp):
    return int(resp[2].split()[-1])


def _get_shared(resp):
    return int(resp[3].split()[-1])


def _get_iterations(resp):
    return resp[4].split()[-1]


def _get_control_sums(resp):
    return ', '.join(resp[5:])


class CfpqResponse:
    def __init__(self, time, rss, vms, shared, iterations, control_sums):
        self.time = time
        self.rss = rss
        self.vms = vms
        self.shared = shared
        self.iterations = iterations
        self.control_sums = control_sums


def cfpq_query(algo: str, graph_name: str, grammar_path: str, redis: Redis):
    resp = [s.decode('UTF-8') for s in redis.execute_command(COMMON_CMD, algo, graph_name, grammar_path)]
    return CfpqResponse(_get_time(resp), _get_rss(resp), _get_vms(resp),
                        _get_shared(resp), _get_iterations(resp), _get_control_sums(resp))
