from collections import defaultdict
from datetime import datetime

from ..csvutil.reader import csv_file_iter

__all__ = []
def export(func):
    __all__.append(func.__name__)
    return func



class Mapper(object):
    NAME = "Mapper"

    @property
    def add_fields(self):
        return self._add_fields

class MapReducer(object):
    NAME = "MapReducer"

    @property
    def add_fields(self):
        return self._add_fields


@export
class Join(Mapper):
    """
    Plain old MapJoin
    """
    NAME = "Join"

    def __init__(self,
                 join_file=None,
                 join_key=None,
                 fields=None,
                 missing_key=None
                 ):
        self._join_file = join_file
        self._join_key = join_key
        self._fields = fields
        self._data = self._read_join_file(join_file)
        self._add_fields = fields

        if missing_key is None:
            self._missing_key = []
        else:
            self._missing_key = [str(missing_key)]


    @property
    def add_fields(self):
        return self._add_fields

    def _get_key(self, example):
        return ",".join([getattr(example, k) for k in self._join_key])

    def _read_join_file(self, filename):
        data = defaultdict(dict)
        with open(filename) as infile:
            for example in csv_file_iter(infile):
                key = self._get_key(example)
                for field in self._fields:
                    data[field][key] = data[field].get(key, []) + [getattr(example, field)]

        return data

    def __call__(self, examples):
        for example in examples:
            for field in self._add_fields:
                #print "field=%s" % field
                key = self._get_key(example)
                value = " ".join(self._data[field].get(key, self._missing_key))
                setattr(example, field, value)
                #print example

@export
class ProcessGeoData(Mapper):
    """
    Mapper parsing geo data
    """

    NAME = "ProcessGeoData"
    def __init__(self, field="geo_location"):
        self._field = field
        self._add_fields = ["geo_country", "geo_state", "geo_dma"]

    def __call__(self, examples):

        for example in examples:
            geo_data = getattr(example, self._field).split(">")
            country, state, dma = '', '', ''
            if geo_data:
                country = geo_data[0]
            if len(geo_data) >= 2:
                state = geo_data[1]
            if len(geo_data) >= 3:
                dma = geo_data[2]

            example.geo_country = country
            example.geo_state = state
            example.geo_dma = dma


@export
class ProcessTimestamp(Mapper):

    NAME = "ProcessTimeStamp"
    def __init__(self, field="timestamp"):
        self._field = field
        self._add_fields = ["date_weekday", "date_hour"]

    def __call__(self, examples):
        for example in examples:
            d = datetime.fromtimestamp(float(getattr(example, self._field)) / 1000.0)
            example.date_weekday = str(d.weekday())
            example.date_hour = str(d.hour)


@export
class CountAdsInBlock(MapReducer):
    """
    This is a pure reducer, i.e. we have to guarantee
    that all examples with one key are in a batch
    """

    NAME = "CountAdsInBlock"
    def __init__(self):
        self._add_fields = ["ads_count"]

    def __call__(self, examples_group):
        ads_count = len(examples_group)
        for example in examples_group:
            example.ads_count = ads_count


@export
class ProcessMissing(Mapper):
    NAME = "ProcessMissing"
    def __init__(self, columns=None, missing_key="-1"):
        self._columns = columns or []
        self._missing_key = missing_key
        self._add_fields = []

    def __call__(self, examples):

        for example in examples:
            check_columns = self._columns or example.keys()
            for col in check_columns:
                value = getattr(example, col)
                if not value:
                    setattr(example, col, self._missing_key)


def ctr_func(clicks, shows, a=1.0, ctr0=1/5.0):

    if clicks == 0.0 and shows == 0.0:
        ctr = ctr0 # missing value
    else:
        ctr = (clicks + a) / (shows + a / ctr0)
    return ctr

@export
class ComputeStatFactors(Mapper):

    NAME = "ComputeStatFactors"
    def __init__(self, stat_keys, smooth_conf=None, ctr0=0.2, online=False):
        self._stat_keys = stat_keys

        self._add_fields = []
        for stat_key in stat_keys:
            self._add_fields.append("ctr_%s" % stat_key)
            #self._add_fields.append("ctr_stat_%s_sm2" % stat_key)

        self._smooth_conf = smooth_conf or {}
        self._ctr0 = ctr0
        self._online = False
        if online:
            self._shows_pattern = "shows_%s"
            self._clicks_pattern = "clicks_%s"
        else:
            self._shows_pattern = "%s_clicks"
            self._clicks_pattern = "%s_shows"

    def _get_key_shows(self, example, key):
        value = getattr(example, self._shows_pattern % key)
        if not value:
            return 0.0
        else:
            return float(value)

    def _get_key_clicks(self, example, key):
        value = getattr(example, self._clicks_pattern % key)
        if not value:
            return 0.0
        else:
            return float(value)

    def __call__(self, examples):

        for example in examples:
            #print example.keys()
            for stat_key in self._stat_keys:
                #print stat_key
                shows = self._get_key_shows(example, stat_key)
                clicks = self._get_key_clicks(example, stat_key)

                ctr0 = self._ctr0
                if stat_key in self._smooth_conf:
                    smooth_key = self._smooth_conf[stat_key]
                    parent_shows = self._get_key_shows(example, smooth_key)
                    parent_clicks = self._get_key_clicks(example, smooth_key)
                    ctr0 = ctr_func(parent_clicks, parent_shows, 0.5, ctr0=self._ctr0)

                #XXX: magic consts (smoothing)
                ctr = ctr_func(clicks, shows, 0.5, ctr0=ctr0)
                #ctr2 = ctr_func(clicks, shows, 2.0, ctr0=ctr0)
                setattr(example, "ctr_%s" % stat_key, str(ctr))
                #setattr(example, "ctr_stat_%s_sm2" % stat_key, str(ctr2))


@export
class ComputeRelCTR(Mapper):

    NAME = "ComputeRelCTR"

    def __init__(self, ctr0=0.2):

        #XXX: hardcoding
        stat_keys = [
            ("document_id_ad_id_1", "document_id_1"),
            ("document_id_campaign_id_1", "document_id_1"),
            ("source_id_ad_id_1", "source_id_1"),
            ("source_id_campaign_id_1", "source_id_1")
        ]

        self._add_fields = []
        for stat_key, hit_key in stat_keys:
            self._add_fields.append("ctr_%s_rel" % stat_key)

        self._ctr0 = ctr0


    def _get_ctr(self, example, key):
        value = getattr(example, "ctr_%s" % key)
        if not value:
            return -1.0
        else:
            return float(value)

    def __call__(self, examples):

        for example in examples:
            # print example.keys()
            for stat_key, hit_key in self._stat_keys:
                rel_ctr = self._get_ctr(example, stat_key) / self._get_ctr(example, hit_key)
                setattr(example, "ctr_%s_rel" % stat_key, str(rel_ctr))


