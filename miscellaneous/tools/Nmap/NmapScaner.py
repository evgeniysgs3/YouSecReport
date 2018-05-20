from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException


HTML_HEADER = """
<!DOCTYPE html>
<html>
<head>
<style>
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #dddddd;
}
</style>
</head>
<body>
"""

HTML_TAIL = """
</body>
</html>
"""

# start a new nmap scan on localhost with some specific options
def do_scan(targets, options):
    parsed = None
    nmproc = NmapProcess(targets, options)
    rc = nmproc.run()
    if rc != 0:
        print("nmap scan failed: {0}".format(nmproc.stderr))
    print(type(nmproc.stdout))

    try:
        parsed = NmapParser.parse(nmproc.stdout)
    except NmapParserException as e:
        print("Exception raised while parsing scan: {0}".format(e.msg))

    return parsed


# write scan results from a nmap report to file
def write_report(nmap_report, report_name):
    for host in nmap_report.hosts:
        if len(host.hostnames):
            tmp_host = host.hostnames.pop()
        else:
            tmp_host = host.address

        report = h2("Nmap {0} ( http://nmap.org ) scan report for {1} ({2})".format(
            nmap_report.version,
            tmp_host,
            host.address))

        report += """<table>
        <tr>
        <th>PORT</th>
        <th>PROTOCOL</th>
        <th>STATE</th> 
        <th>SERVICE</th>
        <th>BANNER</th>
        </tr>"""

        for serv in host.services:
            report += table_service_rep(serv)
        report += "</table>"
    out_report = HTML_HEADER + report + HTML_TAIL

    with open(report_name + '.html', 'w') as f:
        f.write(out_report)


def table_service_rep(serv):
    table = "<tr><td>" + str(serv.port) + "</td>"
    table += "<td>" + serv.protocol + "</td>"
    table += "<td>" + serv.state + "</td>"
    table += "<td>" + serv.service + "</td>"
    table += "<td>" + serv.banner + "</td>"
    table += "</tr>"
    return table

def h2(string):
    return "<h2>" + string + "</h2>"


if __name__ == "__main__":
    
    with open('list_ip.txt', 'r') as list_ip_file:
        list_ip = list_ip_file.read()
    for ip in list_ip.split('\n'):
        report = do_scan(ip, "-sV")
        if report:
            write_report(report, ip)
        else:
            print("No results returned")