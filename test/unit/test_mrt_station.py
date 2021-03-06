from datetime import datetime

from mrt.core.mrt_station import MRTStation
from mrt.utils.consts import OPEN_DATE_FORMAT
from mrt.core.mrt_line_tag import LineTags


class TestMRTStation:
    def test_init(self):
        """
        Test init a station object
        """
        s1 = MRTStation('NS4', 'Choa Chu Kang', datetime.strptime('10 March 1990', OPEN_DATE_FORMAT))
        assert s1.key == 'NS4'
        assert s1.name == 'Choa Chu Kang'
        assert s1.open_date == datetime.strptime('10 March 1990', OPEN_DATE_FORMAT)
        assert s1.line_tag == LineTags['NS']
