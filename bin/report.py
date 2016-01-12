# -*- coding:utf-8 -*-
__author__ = 'xuekj'
from util import get_dir_files
from config import config
from template import report_html_header
from template import report_overall_html_table
from template import report_top_request_html_table_header
from template import report_top_request_html_table_body
from template import report_html_end
from template import index_html_header
from template import index_html_li
from template import index_html_end
from template import url_html_header
from template import url_html_table_body
from template import url_html_end


def generate_web_log_parser_report(data):
    if config.goaccess_flag:
        data.setdefault('goaccess_file', data.get('source_file')+'_GoAccess.html')
        data.setdefault('goaccess_title', u'查看GoAccess生成报告'.encode('utf-8'))
    else:
        data.setdefault('goaccess_file', '#')
        data.setdefault('goaccess_title', u'GoAccess报告已设置为无效，无法查看'.encode('utf-8'))
    html_body = report_overall_html_table  % data

    html_body += report_top_request_html_table_header % {'web_log_urls_file': data.get('source_file')+'_urls.html'}

    url_data_list = data.get('url_data_list')
    for url_data in url_data_list:
        url_data_dict = {'url': url_data.url.split()[1], 'pv': url_data.pv, 'ratio': url_data.ratio,
                         'response_peak': url_data.peak,
                         'protocol': url_data.url.split()[2].replace('"', ''),
                         'method': url_data.url.split()[0].replace('"', '')}
        html_body += report_top_request_html_table_body % url_data_dict
    
    pvs = data.get('hours_hits')
    hours_pv = {'h0': pvs['00'],
            'h1': pvs['01'],
            'h2': pvs['02'],
            'h3': pvs['03'],
            'h4': pvs['04'],
            'h5': pvs['05'],
            'h6': pvs['06'],
            'h7': pvs['07'],
            'h8': pvs['08'],
            'h9': pvs['09'],
            'h10': pvs['10'],
            'h11': pvs['11'],
            'h12': pvs['12'],
            'h13': pvs['13'],
            'h14': pvs['14'],
            'h15': pvs['15'],
            'h16': pvs['16'],
            'h17': pvs['17'],
            'h18': pvs['18'],
            'h19': pvs['19'],
            'h20': pvs['20'],
            'h21': pvs['21'],
            'h22': pvs['22'],
            'h23': pvs['23'],
            'date': data.get('date')
            }
    html = report_html_header + html_body + report_html_end % hours_pv
    html_file = '../result/report/'+data.get('source_file')+'.html'
    with open(html_file, 'w') as f:
        f.write(html)

def generate_web_log_parser_urls(data):
    html = url_html_header % data
    for index, url_data in enumerate(sorted(data.get('urls'))):
        html += url_html_table_body % {'url': url_data.split()[1], 'num': index+1,
                'method': url_data.split()[0].replace('"', ''),
                'protocol': url_data.split()[2].replace('"', '')}
    html += url_html_end
    html_file = '../result/urls/'+data.get('source_file')+'_urls.html'
    with open(html_file, 'w') as f:
        f.write(html)

def update_index_html():
    html = index_html_header
    for report_file in sorted(get_dir_files('../result/report/')):
        if report_file.find('GoAccess') != -1 or report_file.find('.git') != -1 :
            pass
        else:
            html += index_html_li % {'web_log_parser_file': report_file}
    html += index_html_end

    with open('../result/index.html', 'w') as f:
        f.write(html)

