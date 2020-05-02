from datetime import date
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from dateutil.parser import parse

tenant_id_regex = '[a-z0-9_]+'
timezone_jst = timezone(timedelta(hours=9))


def datetime_jst_now() -> datetime:
    """JSTタイムゾーンの現在時刻のdatetimeオブジェクトを生成する"""
    return datetime.now(tz=timezone_jst)


def datetime_jst_now_delta(
        weeks=0, days=0, hours=0, minutes=0,
        seconds=0, microseconds=0) -> datetime:
    delta = timedelta(
            weeks=weeks, days=days, hours=hours,
            minutes=minutes, seconds=seconds,
            microseconds=microseconds)
    return datetime.now(tz=timezone_jst) + delta


def datetime_jst(year, month, day, hour=0, minute=0, second=0, microsecond=0):
    """JSTタイムゾーンのdatetimeオブジェクトを生成する"""
    return datetime(year,
                    month,
                    day,
                    hour,
                    minute,
                    second,
                    microsecond,
                    tzinfo=timezone_jst)


def timestamp_full(dt=None):
    """マイクロ秒単位のタイムスタンプ文字列を生成する"""
    if dt is None:
        dt = datetime_jst_now()
    return dt.strftime('%Y%m%d%H%M%S%f')


def parse_timestamp_full(ts_str: str) -> datetime:
    """マイクロ秒単位のタイムスタンプ文字列をdatetimeにパースする。"""
    return datetime.strptime(ts_str, '%Y%m%d%H%M%S%f')


def parse_datetime_as_jst(dt_str: str) -> datetime:
    """
    時刻文字列のパース処理。
    タイムゾーン指定の無い文字列は日本時間とみなす。
    タイムゾーン指定があれば日本時間に変換する。
    """
    dt = parse(dt_str)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone_jst)
    else:
        return dt.astimezone(timezone_jst)


def parse_date(date_str: str) -> date:
    """
    日付文字列のパース処理
    """
    d = parse(date_str)
    return d.date()
