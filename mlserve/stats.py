from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from statistics import mean
from typing import Deque, Dict, Any


@dataclass
class RequestTiming:
    status: int
    start_time: datetime
    duration: float


def factory(maxlen: int=1000) -> Deque[RequestTiming]:
    return deque(maxlen=maxlen)


@dataclass
class _Stats:
    success: int = 0
    error: int = 0
    timings: Deque[RequestTiming] = field(default_factory=factory)

    def mean_resp_time(self) -> float:
        series = [t.duration for t in self.timings if t.status < 400]
        return mean(series) if series else 0

    def formatted(self) -> Dict[str, Any]:
        # TODO: format time series datapoints
        f = {
            'success': self.success,
            'error': self.error,
            'mean_resp_time': round(self.mean_resp_time(), 4)
        }
        return f


class ModelStats(_Stats):

    def log_data_point(self, t: RequestTiming) -> None:
        if t.status < 400:
            self.success += 1
        else:
            self.error += 1
        self.timings.append(t)


class AggStats(_Stats):

    @classmethod
    def from_models_stats(cls, stats_map: Dict[str, ModelStats]) -> 'AggStats':
        agg_stats = cls()
        all_timings = []
        for stat in stats_map.values():
            agg_stats.success += stat.success
            agg_stats.error += stat.error
            all_timings.extend(list(stat.timings))

        # TODO: implement merge functions of sorted timings
        timings = sorted(all_timings, key=lambda v: v.start_time)[-1000:]
        agg_stats.timings.extend(timings)
        return agg_stats
