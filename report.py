import io

import xlsxwriter

from db import (
    get_stats,
)


def generate_report(metric_uuid, metric_name):
    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output, {"in_memory": True})
    worksheet = workbook.add_worksheet('Sheet1')

    # table headers
    header = workbook.add_format({'italic': True, 'border': 1, 'align': 'center'})
    worksheet.write(0, 0, 'Value', header)
    worksheet.write(0, 1, 'Created At', header)
    worksheet.set_column("A:B", 16)
    worksheet.freeze_panes(1, 0)

    # table
    stats = get_stats(metric_uuid)

    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm'})

    row = 1

    for value, dt in stats:
        worksheet.write_number(row, 0, value)
        worksheet.write_datetime(row, 1, dt, date_format)
        row += 1

    # chart
    stats_len = len(stats)

    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
        'categories': f'=Sheet1!$B$2:$B${stats_len + 1}',
        'values': f'=Sheet1!$A$2:$A${stats_len + 1}',
        'name': f'{metric_name} over Time',
    })
    chart.set_x_axis({
        'name': 'Date',
        'date_axis': True,
        'num_format': 'yyyy-mm-dd',
    })
    chart.set_y_axis({'name': 'Value'})

    worksheet.insert_chart('D2', chart)

    workbook.close()

    output.seek(0)
    return output
