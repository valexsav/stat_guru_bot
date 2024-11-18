import io

import xlsxwriter

from db import (
    get_stats,
)


def add_days_worksheet(workbook, metric_name, stats):
    worksheet_name = 'Days'
    worksheet = workbook.add_worksheet(worksheet_name)

    # table headers
    header = workbook.add_format({'italic': True, 'border': 1, 'align': 'center'})
    worksheet.write(0, 0, 'Value', header)
    worksheet.write(0, 1, 'Created At', header)
    worksheet.set_column("A:B", 16)
    worksheet.freeze_panes(1, 0)

    # table
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
        'categories': f'={worksheet_name}!$B$2:$B${stats_len + 1}',
        'values': f'={worksheet_name}!$A$2:$A${stats_len + 1}',
        'line': {'color': '#4A8F31'},
        'marker': {'type': 'circle'},
        'data_labels': {
            'value': True,
            'font': {'rotation': 45, 'size': 6, 'bold': True},
        },
    })
    chart.set_x_axis({
        'name': 'Date',
        'date_axis': True,
        'num_format': 'yyyy-mm-dd',
        'name_font': {'size': 8},
        'num_font': {'size': 8},
    })
    chart.set_y_axis({
        'name': 'Value',
        'name_font': {'size': 8},
        'num_font': {'size': 8},
    })
    chart.set_legend({'none': True})

    worksheet.insert_chart('D2', chart, {
        'x_scale': 1.2,
        'y_scale': 1.2,
    })


def add_weeks_worksheet(workbook, metric_name, stats):

    week_stats = {}
    for stat in stats:
        year, week, _ = stat[1].isocalendar()
        key = f'{year}/{week}'
        week_stats[key] = week_stats.get(key, 0) + stat[0]

    worksheet_name = 'Weeks'
    worksheet = workbook.add_worksheet(worksheet_name)

    # table headers
    header = workbook.add_format({'italic': True, 'border': 1, 'align': 'center'})
    worksheet.write(0, 0, 'Value', header)
    worksheet.write(0, 1, 'Created At (Week)', header)
    worksheet.set_column("A:B", 16)
    worksheet.freeze_panes(1, 0)

    # table
    row = 1

    for week, value in week_stats.items():
        worksheet.write_number(row, 0, value)
        worksheet.write_string(row, 1, week)
        row += 1

    # chart
    stats_len = len(week_stats)

    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
        'categories': f'={worksheet_name}!$B$2:$B${stats_len + 1}',
        'values': f'={worksheet_name}!$A$2:$A${stats_len + 1}',
        'line': {'color': '#4A8F31'},
        'marker': {'type': 'circle'},
        'data_labels': {
            'value': True,
            'font': {'size': 6, 'bold': True},
        },
    })
    chart.set_x_axis({
        'name': 'Week',
        'reverse': True,
        'name_font': {'size': 8},
        'num_font': {'size': 8},
    })
    chart.set_y_axis({
        'name': 'Value',
        'name_font': {'size': 8},
        'num_font': {'size': 8},
    })
    chart.set_legend({'none': True})

    worksheet.insert_chart('D2', chart, {
        'x_scale': 1.2,
        'y_scale': 1.2,
    })


def add_months_worksheet(workbook, metric_name, stats):

    month_stats = {}
    for stat in stats:
        key = f'{stat[1].year}/{stat[1].month}'
        month_stats[key] = month_stats.get(key, 0) + stat[0]

    worksheet_name = 'Months'
    worksheet = workbook.add_worksheet(worksheet_name)

    # table headers
    header = workbook.add_format({'italic': True, 'border': 1, 'align': 'center'})
    worksheet.write(0, 0, 'Value', header)
    worksheet.write(0, 1, 'Created At (Month)', header)
    worksheet.set_column("A:B", 16)
    worksheet.freeze_panes(1, 0)

    # table
    row = 1

    for month, value in month_stats.items():
        worksheet.write_number(row, 0, value)
        worksheet.write_string(row, 1, month)
        row += 1

    # chart
    stats_len = len(month_stats)

    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
        'categories': f'={worksheet_name}!$B$2:$B${stats_len + 1}',
        'values': f'={worksheet_name}!$A$2:$A${stats_len + 1}',
        'line': {'color': '#4A8F31'},
        'marker': {'type': 'circle'},
        'data_labels': {
            'value': True,
            'font': {'size': 6, 'bold': True},
        },
    })
    chart.set_x_axis({
        'name': 'Month',
        'reverse': True,
        'name_font': {'size': 8},
        'num_font': {'size': 8},
    })
    chart.set_y_axis({
        'name': 'Value',
        'name_font': {'size': 8},
        'num_font': {'size': 8},
    })
    chart.set_legend({'none': True})

    worksheet.insert_chart('D2', chart, {
        'x_scale': 1.2,
        'y_scale': 1.2,
    })


def generate_report(metric_uuid, metric_name):
    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output, {"in_memory": True})

    stats = get_stats(metric_uuid)
    add_days_worksheet(workbook, metric_name, stats)
    add_weeks_worksheet(workbook, metric_name, stats)
    add_months_worksheet(workbook, metric_name, stats)

    workbook.close()

    output.seek(0)
    return output
