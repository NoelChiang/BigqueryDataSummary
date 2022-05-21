# Defined chart folder
chart_resource_folder = "charts/"
# Defined chart output path
chart_path_daily_session = chart_resource_folder + "daily_session_chart.png"
chart_path_daily_purchase = chart_resource_folder + "daily_purchase_chart.png"

# Update notes
update_logs = {
    '2021/06/04': ['New chart created: User activity in home page'],
    '2021/07/14': ['Bug fix: Incorrect title'],
}

update_date = max(list(update_logs.keys()))
update_date_phrase = 'Latest update at ' + update_date

update_scopes = 'Update contents: \n'
for note in update_logs[update_date]:
    update_scopes = update_scopes + '* ' + note + '\n'


def get_mail_notify_attachments():
    return [chart_path_daily_purchase]
