__all__ = ["get_head_doc", "get_table", "wraper_html_tag", "DOCTYPE"]

DOCTYPE = "<!DOCTYPE html>\n"


def get_close_tag(tag):
    close_tag = list(tag)
    close_tag.insert(1, "/")
    return "".join(close_tag)


def insert_prop(tag, prop):
    prop_with_space = " " + prop
    upd_tag = list(tag)
    upd_tag.insert(-1, prop_with_space)
    return "".join(upd_tag)


def wraper_tag_anything(open_tag, body, close_tag=None, sep="\n", prop=None):
    if not close_tag:
        close_tag = get_close_tag(open_tag)

    if prop is not None:
        open_tag = insert_prop(open_tag, prop)

    return sep.join([open_tag, body, close_tag])


def wraper_html_tag(tag, body_str, sep="\n", prop=None):
    html_tags = ["<html>",
                 "<head>",
                 "<style>",
                 "<body>",
                 "<tr>",
                 "<th>",
                 "<h2>",
                 "<table>",
                 "<table>",
                 "<tbody>",
                 "<td>"
                 ]

    if tag not in html_tags:
        raise "This tag not support"

    return wraper_tag_anything(tag, body_str, sep=sep, prop=prop)


def get_head_doc():
    table_style = "table {font-family: arial, sans-serif; border-collapse: collapse; width: 100%;}"
    tdth_description = "td, th {border: 1px solid #dddddd; text-align: left; padding: 8px;}"
    tr_description = "tr:nth-child(even) {background-color: #dddddd;}"

    head_doc = "\n".join([table_style, tdth_description, tr_description])
    head_doc = wraper_html_tag("<style>", head_doc)
    head_doc = wraper_html_tag("<head>", head_doc)

    return head_doc


def get_head_table(head_lst):
    head_table = [wraper_html_tag("<th>", header.upper(), sep="", prop=width) for header, width in head_lst.items()]
    head_table = "".join(head_table)
    head_table = wraper_html_tag("<tr>", head_table, sep="")
    return head_table


def get_body_table(head_lst, reports):
    body_table = []
    for report in reports:
        table_string = []
        for notation in head_lst:
            try:
                table_cell = str(report[notation])
            except KeyError:
                table_cell = '-'
            table_cell = wraper_html_tag("<td>", table_cell, sep="")
            table_string.append(table_cell)
        table_string = "".join(table_string)
        table_string = wraper_html_tag("<tr>", table_string, sep="")
        body_table.append(table_string)
    return body_table


def get_table(head_lst, reports):
    head_table = get_head_table(head_lst)
    body_table = get_body_table(head_lst, reports)

    body_table.insert(0, head_table)
    body_table = "\n".join(body_table)
    body_table = wraper_html_tag("<tbody>", body_table)
    table = wraper_html_tag("<table>", body_table)
    return table
