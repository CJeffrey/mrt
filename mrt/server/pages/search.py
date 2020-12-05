"""
The Page for search. The basic version
"""
import logging

from datetime import datetime
from flask import request, render_template

from mrt.server.mrt_app import mrt_app
from mrt.core.mrt_solution import MRTSolution

logger = logging.getLogger(__name__)

WEB_TIME_FORMAT = '%Y-%m-%dT%H:%M'


@mrt_app.route('/search_basic', methods=['GET'])
def search_basic_get():
    """

    :return: the get html for this page
    """
    # call mrt core to get the mrt_map
    mrt_solution = MRTSolution()
    mrt_map = mrt_solution.mrt_map
    data = mrt_map.get_nodes_links()
    return render_template('search_basic.html', data=data)


@mrt_app.route('/search_basic', methods=['POST'])
def search_basic_post():
    """

    :return: the post html for this page
    """
    src_name = request.form['src_name']
    des_name = request.form['des_name']
    time = request.form['time']

    try:
        start_time = datetime.strptime(time, WEB_TIME_FORMAT)
    except ValueError:
        logger.error('can not analyze time from web: {}, use now instead'.format(time))
        start_time = datetime.now()

    # call mrt core to get the travel plan
    mrt_solution = MRTSolution()
    travel_plan = mrt_solution.search_by_name(src_name, des_name, start_time)
    readable_plan = travel_plan.get_readable_plan()

    mrt_map = mrt_solution.mrt_map
    data = mrt_map.get_nodes_links()

    payloads = {
        'src_name': src_name,
        'des_name': des_name,
        'time': start_time.strftime(WEB_TIME_FORMAT),
        'message': readable_plan.message,
        'data': data
    }

    if readable_plan.is_reachable():
        outcomes = readable_plan.get_readable_outcome()
        payloads.update({'outcomes': outcomes})

    return render_template('search_basic.html', **payloads)
