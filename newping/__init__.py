import os
import simplejson as json
import datetime
import pyping

# import cairocffi
# cairocffi.install_as_pycairo()

try:
    import pygal
except ImportError:
    pygal = None
    print "You have no Pygal installed. No plots will be created."


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(ROOT_DIR, 'ip.json'), 'r') as confFile:
    conf = json.load(confFile)

DATA_DIR = os.path.realpath(
    os.path.join(ROOT_DIR, '../data')
)

POINT_FORMAT = '{timestamp};{region};{value:0.2f}'


def generate_graph():

    if not pygal:
        return

    today = datetime.datetime.now()
    storage_filepath = _get_storage_filepath()
    graph_filepath = os.path.join(
        DATA_DIR, 'ping_%s.png' % today.strftime('%b_%d_%Y'))

    line_chart = pygal.Line()
    line_chart.title = 'Ping state %s (RTT in ms)' % (
        today.strftime('%x'),
    )
    line_chart.x_labels = ["%s" % x for x in range(0, 24)]

    existed_points = {}

    with open(storage_filepath, 'r') as storage_file:
        while True:
            _point = storage_file.readline().strip("\n")

            if not _point:
                break

            (point_timestamp, point_region, point_value) = _point.split(';')
            point_datetime = datetime.datetime.strptime(
                point_timestamp, "%Y-%m-%d %H:%M:%S.%f")
            hour = point_datetime.hour

            if point_datetime.date() != today.date():
                continue

            try:
                existed_points[point_region]
            except KeyError:
                existed_points[point_region] = {}
            try:
                existed_points[point_region][hour]
            except KeyError:
                existed_points[point_region][hour] = []

            existed_points[point_region][hour].append(float(point_value))

    for region in conf:
        hour_avg_values = []

        for hour_r in range(0, 24):
            hour_avg_val = None

            try:
                all_values = existed_points[region['region']['code']][hour_r]
            except KeyError:
                continue
            else:
                hour_avg_val = sum(all_values) / len(all_values)

            hour_avg_values.append(hour_avg_val)

        line_chart.add(region['region']['name'], hour_avg_values)

    line_chart.render_to_png(graph_filepath)


def _get_storage_filepath():
    now = datetime.datetime.now()
    filename = 'ping_data_%s.txt' % (now.strftime('%b_%d_%Y'), )
    filepath = os.path.join(DATA_DIR, filename)
    return filepath


def _save_points(points):
    if not len(points):
        return

    with open(_get_storage_filepath(), 'a+') as storage_file:
        for p in points:
            storage_file.write(p + "\n")


def main():
    timestamp = datetime.datetime.now()
    point_strings = []

    for region in conf:
        ip_list = region['ip_list']

        region_values = []

        for ip in ip_list:
            r = pyping.ping(ip)
            if r.ret_code == 0:
                region_values.append(float(r.avg_rtt))

        point_str = POINT_FORMAT.format(
            timestamp=str(timestamp), region=region['region']['code'],
            value=sum(region_values) / len(region_values))
        point_strings.append(point_str)

    _save_points(point_strings)
    generate_graph()
