# -*- coding: utf-8 -*-
from JobBrowserBFF.TestBase import TestBase
from JobBrowserBFF.schemas.Schema import Schema
from JobBrowserBFF.Validation import Validation
import unittest

UPSTREAM_SERVICE = 'mock'
ENV = 'mock'
USER_CLASS = 'admin'
TIMEOUT_MS = 10000
# 10/1/19
TIMESTAMP_FROM = 0
# 11/1/19
TIMESTAMP_TO = 1575158400000
TOTAL_COUNT = 55104


class JobBrowserBFFTest(TestBase):
    # Uncomment to skip this test
    # @unittest.skip("skipped test_query_jobs_happy")
    def test_query_jobs_user_happy(self):
        self.set_config('upstream-service', UPSTREAM_SERVICE)
        try:
            impl, context = self.impl_for(ENV, USER_CLASS)
            ret = impl.query_jobs(context, {
                'time_span': {
                    'from': TIMESTAMP_FROM,
                    'to': TIMESTAMP_TO
                },
                'offset': 0,
                'limit': 10,
                'admin': 1
            })
            jobs, found_count, total_count = self.assert_job_query_result_with_count(ret)
            self.assertEqual(found_count, TOTAL_COUNT)
            self.assertEqual(total_count, TOTAL_COUNT)
            self.assertEqual(len(jobs), 10)
        except Exception as ex:
            self.assert_no_exception(ex)

    # Uncomment to skip this test
    # @unittest.skip("skipped test_query_jobs_filters_happy")
    def test_query_jobs_filters_happy(self):
        self.set_config('upstream-service', UPSTREAM_SERVICE)
        cases = [
            {
                'params': {
                    'filter': {
                        'workspace_id': 24614
                    }
                },
                'expected': {
                    'found_count': 5,
                    'total_count': TOTAL_COUNT,
                    'count': 5
                }
            }, {
                'params': {
                    'filter': {
                        'job_id': '59811b41e4b06f68bf751ee3'
                    }
                },
                'expected': {
                    'found_count': 1,
                    'total_count': TOTAL_COUNT,
                    'count': 1
                }
            }, {
                'params': {
                    'filter': {
                        'client_group': 'njs'
                    }
                },
                'expected': {
                    'found_count': 20256,
                    'total_count': TOTAL_COUNT,
                    'count': 10
                }
            },
            {
                'params': {
                    'filter': {
                        'app': 'RAST_SDK/annotate_contigset'
                    }
                },
                'expected': {
                    'found_count': 240,
                    'total_count': TOTAL_COUNT,
                    'count': 10
                }
            }
        ]
        base_params = {
            'time_span': {
                'from': TIMESTAMP_FROM,
                'to': TIMESTAMP_TO
            },
            'offset': 0,
            'limit': 10,
            'admin': 1
        }
        try:
            impl, context = self.impl_for(ENV, USER_CLASS)
            for case in cases:
                params = base_params.copy()
                params.update(case['params'])
                ret = impl.query_jobs(context, params)
                jobs, found_count, total_count = self.assert_job_query_result_with_count(ret)
                self.assertEqual(found_count, case['expected']['found_count'])
                self.assertEqual(total_count, case['expected']['total_count'])
                self.assertEqual(len(jobs), case['expected']['count'])
        except Exception as ex:
            self.assert_no_exception(ex)

    # Different time ranges
    # @unittest.skip("skipped test_query_jobs_time_spans_happy")
    def test_query_jobs_time_spans_happy(self):
        self.set_config('upstream-service', UPSTREAM_SERVICE)
        cases = [{
            # 2015
            'params': {
                'time_span': {
                    'from': 1420070400000,
                    'to': 1451606400000
                },
            },
            'expected': {
                'found_count': 2634,
                'total_count': TOTAL_COUNT,
                'count': 10
            }
        }, {
            # 2016
            'params': {
                'time_span': {
                    'from': 1451606400000,
                    'to': 1483228800000
                },
            },
            'expected': {
                'found_count': 30922,
                'total_count': TOTAL_COUNT,
                'count': 10
            }
        }, {
            # 2017
            'params': {
                'time_span': {
                    'from': 1483228800000,
                    'to': 1514764800000
                },
            },
            'expected': {
                'found_count': 6323,
                'total_count': TOTAL_COUNT,
                'count': 10
            }
        }, {
            # 2018
            'params': {
                'time_span': {
                    'from': 1514764800000,
                    'to': 1546300800000
                },
            },
            'expected': {
                'found_count': 6471,
                'total_count': TOTAL_COUNT,
                'count': 10
            }
        }, {
            # 2019
            'params': {
                'time_span': {
                    'from': 1546300800000,
                    'to': 1577836800000
                },
            },
            'expected': {
                'found_count': 8754,
                'total_count': TOTAL_COUNT,
                'count': 10
            }
        }, {
            # All of time (up to 11/1/19)
            # Note that the found count here should equal the sum of the
            # found counts from all the above.
            'params': {
                'time_span': {
                    'from': 0,
                    'to': 1575158400000
                },
            },
            'expected': {
                'found_count': TOTAL_COUNT,
                'total_count': TOTAL_COUNT,
                'count': 10
            }
        }]
        base_params = {
            'offset': 0,
            'limit': 10,
            'admin': 1
        }
        try:
            impl, context = self.impl_for(ENV, USER_CLASS)
            for case in cases:
                params = base_params.copy()
                params.update(case['params'])
                ret = impl.query_jobs(context, params)
                jobs, found_count, total_count = self.assert_job_query_result_with_count(ret)
                self.assertEqual(found_count, case['expected']['found_count'])
                self.assertEqual(total_count, case['expected']['total_count'])
                self.assertEqual(len(jobs), case['expected']['count'])
        except Exception as ex:
            self.assert_no_exception(ex)

    # Uncomment to skip this test
    # @unittest.skip("skipped test_query_jobs_sort_happy")
    def test_query_jobs_sort_happy(self):
        self.set_config('upstream-service', UPSTREAM_SERVICE)
        cases = [{
            'params': {
                'sort': [
                    {
                        'key': 'created',
                        'direction': 'ascending'
                    }
                ],
            },
            'expected': {
                'found_count': TOTAL_COUNT,
                'total_count': TOTAL_COUNT,
                'count': 10,
                'first': '54b02da8e4b06e6b5555476d',
                'last': '54c5d7b5e4b0c6df765a91aa'
            }
        }, {
            'params': {
                'sort': [
                    {
                        'key': 'created',
                        'direction': 'descending'
                    }
                ],
            },
            'expected': {
                'found_count': TOTAL_COUNT,
                'total_count': TOTAL_COUNT,
                'count': 10,
                'first': '5d94b6f8aa5a4d298c5dc9d7',
                'last': '5d93b034aa5a4d298c5dc9ce'
            }
        }]
        base_params = {
            'time_span': {
                'from': TIMESTAMP_FROM,
                'to': TIMESTAMP_TO
            },
            'offset': 0,
            'limit': 10,
            'admin': 1
        }
        try:
            impl, context = self.impl_for(ENV, USER_CLASS)
            for case in cases:
                params = base_params.copy()
                params.update(case['params'])
                ret = impl.query_jobs(context, params)
                jobs, found_count, total_count = self.assert_job_query_result_with_count(ret)
                self.assertEqual(found_count, case['expected']['found_count'])
                self.assertEqual(total_count, case['expected']['total_count'])
                self.assertEqual(len(jobs), case['expected']['count'])
                self.assertEqual(jobs[0]['job_id'], case['expected']['first'])
                self.assertEqual(jobs[9]['job_id'], case['expected']['last'])
                if case['params']['sort'][0]['direction'] == 'ascending':
                    self.assert_in_ascending_order(jobs, ['state', 'create_at'])
                else:
                    self.assert_in_descending_order(jobs, ['state', 'create_at'])
        except Exception as ex:
            self.assert_no_exception(ex)

    # Uncomment to skip this test
    # @unittest.skip("skipped test_query_jobs_search_happy")
    def test_query_jobs_search_happy(self):
        self.set_config('upstream-service', UPSTREAM_SERVICE)
        cases = [{
            'params': {
                'search': {
                    'terms': ['5980cf6fe4b06f68bf751edd']
                }
            },
            'expected': {
                'found_count': 1,
                'total_count': TOTAL_COUNT,
                'count': 1
            }
        }, {
            'params': {
                'search': {
                    'terms': ['megahit']
                }
            },
            'expected': {
                'found_count': 827,
                'total_count': TOTAL_COUNT,
                'count': 10
            }
        }, {
            'params': {
                'search': {
                    'terms': ['run_megahit']
                }
            },
            'expected': {
                'found_count': 827,
                'total_count': TOTAL_COUNT,
                'count': 10
            }
        }, {
            'params': {
                'search': {
                    'terms': ['annotate_contigset']
                }
            },
            'expected': {
                'found_count': 312,
                'total_count': TOTAL_COUNT,
                'count': 10
            }
        }, {
            'params': {
                'search': {
                    'terms': ['error']
                }
            },
            'expected': {
                'found_count': 34534,
                'total_count': TOTAL_COUNT,
                'count': 10
            }
        }, {
            'params': {
                'search': {
                    'terms': ['abc123']
                }
            },
            'expected': {
                'found_count': 0,
                'total_count': TOTAL_COUNT,
                'count': 0
            }
        }, {
            'params': {
                'search': {
                    'terms': ['eaptest30']
                }
            },
            'expected': {
                'found_count': 19,
                'total_count': TOTAL_COUNT,
                'count': 10
            }
        }]
        base_params = {
            'time_span': {
                'from': TIMESTAMP_FROM,
                'to': TIMESTAMP_TO
            },
            'offset': 0,
            'limit': 10,
            'admin': 1
        }
        try:
            impl, context = self.impl_for(ENV, USER_CLASS)
            for case in cases:
                params = base_params.copy()
                params.update(case['params'])
                ret = impl.query_jobs(context, params)
                jobs, found_count, total_count = self.assert_job_query_result_with_count(ret)
                self.assertEqual(found_count, case['expected']['found_count'])
                self.assertEqual(total_count, case['expected']['total_count'])
                self.assertEqual(len(jobs), case['expected']['count'])
        except Exception as ex:
            self.assert_no_exception(ex)
