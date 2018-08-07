from datetime import datetime
from mlserve.stats import ModelStats, AggStats, RequestTiming


def test_request_timing_ctor():
    dt = datetime(2018, 8, 5, 12, 5, 47, 000000)
    rt = RequestTiming(200, dt, 0.01)
    assert rt.status == 200


def test_model_stats_ctor():
    model_stats = ModelStats()
    assert model_stats.success == 0
    assert model_stats.error == 0
    assert model_stats.mean_resp_time() == 0
    assert len(model_stats.timings) == 0
    expected = {
        'success': 0,
        'error': 0,
        'mean_resp_time': 0,
        }
    assert model_stats.formatted() == expected


def test_model_stats_log_data_point():
    dt = datetime(2018, 8, 5, 12, 5, 47, 000000)
    rt1 = RequestTiming(200, dt, 0.01)
    dt = datetime(2018, 8, 5, 12, 6, 47, 000000)
    rt2 = RequestTiming(200, dt, 0.01)
    model_stats = ModelStats()
    model_stats.log_data_point(rt1)
    model_stats.log_data_point(rt2)

    assert model_stats.success == 2
    assert model_stats.error == 0
    assert model_stats.mean_resp_time() == 0.01


def test_agg_stats_ctor():
    agg_stats = AggStats()
    assert agg_stats.success == 0
    assert agg_stats.error == 0
    assert agg_stats.mean_resp_time() == 0
    assert len(agg_stats.timings) == 0

    expected = {
        'success': 0,
        'error': 0,
        'mean_resp_time': 0,
        }
    assert agg_stats.formatted() == expected

    model_stats1 = ModelStats()
    model_stats2 = ModelStats()

    stats_map = {'name1': model_stats1, 'name2': model_stats2}
    agg_stats = AggStats.from_models_stats(stats_map)
    assert agg_stats.success == 0
    assert agg_stats.error == 0
    assert agg_stats.mean_resp_time() == 0
    assert len(agg_stats.timings) == 0
