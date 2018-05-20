from .common_data import *


def nikto_rep_generate(report):
    table_header = ["id", "OSVDB", "method", "msg"]

    head_rep = get_head_doc()

    banner = "Nikto scan report for ip: {}, host: {}, port: {}".format(report["ip"], report["host"], report["port"])
    banner = wraper_html_tag("<h2>", banner, sep="")

    table = get_table(table_header, report["vulnerabilities"])

    body = "\n".join([banner, table])
    body = wraper_html_tag("<body>", body)

    report = "\n".join([head_rep, body])
    report = wraper_html_tag("<html>", report)

    return DOCTYPE + report
