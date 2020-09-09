from datetime import datetime
from dateutil import parser, tz

from elastalert.enhancements import BaseEnhancement
from elastalert.enhancements import DropMatchException


class HourRangeEnhancement(BaseEnhancement):
    def process(self, match):
        timestamp = None
        try:
            timestamp = parser.parse(match['@timestamp'])
        except Exception:
            try:
                timestamp = parser.parse(match['timestamp'])
            except Exception:
                pass
        if timestamp is not None:
            timestamp = timestamp.replace(tzinfo=tz.gettz('UTC'))
            timestamp = timestamp.astimezone(tzinfo=tz.gettz('Asia/Jerusalem')).time()
            time_start = parser.parse(self.rule['start_time']).time()
            time_end = parser.parse(self.rule['end_time']).time()
            if(self.rule['drop_if'] == 'outside'):
                if timestamp < time_start or timestamp > time_end:
                    raise DropMatchException()
            elif(self.rule['drop_if'] == 'inside'):
                if timestamp >= time_start and timestamp <= time_end:
                    raise DropMatchException()
