from datetime import datetime
from flask import request, render_template

from mrt.server.mrt_app import mrt_app
from mrt.core.mrt_solution import MRTSolution

TIME_FORMAT = '%Y-%m-%dT%H:%M'


@mrt_app.route('/search_basic', methods=['GET'])
def search_basic_get():
    return render_template('search_basic.html')


@mrt_app.route('/search_basic', methods=['POST'])
def search_basic_post():
    src_name = request.form['src_name']
    des_name = request.form['des_name']
    time_str = request.form['time_str']

    start_time = datetime.now()

    mrt_solution = MRTSolution()
    travel_plan = mrt_solution.search_by_name(src_name, des_name, start_time)
    readable_plan = travel_plan.get_readable_plan()
    outcomes = readable_plan.get_readable_outcome()

    return render_template('search_basic.html',
                           src_name=src_name,
                           des_name=des_name,
                           time_str=time_str,
                           outcomes=outcomes)
