#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import sys
#import httplib
#import urllib
import socket
import requests
import time
import json
import urlparse
import logging


# Use Token, check https://support.dnspod.cn/Kb/showarticle/tsid/227/


def getdomainid(idtoken, domain):
    params = dict(
            login_token = idtoken,
            format = 'json',
            )
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/json', 'User-Agent': 'dnspod-python/0.01 (pzping@gmail.com)'}
    resp = requests.post('https://dnsapi.cn/domain.list', data = params, headers = headers)
    logging.debug(json.dumps(resp.json(), indent = 1))
    for item in resp.json()['domains']:
        if item['name'] == domain:
            id = item['id']
    logging.info('Domain ID: %s'% id)
    return id

def getrecordid(idtoken, domain_id, sub_domain):
    params = dict(
            login_token = idtoken,
            sub_domain = sub_domain,
            domain_id = domain_id,
            format = 'json',
            )
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/json', 'User-Agent': 'dnspod-python/0.01 (pzping@gmail.com)'}
    resp = requests.post('https://dnsapi.cn/record.list', data = params, headers = headers)
    logging.debug(json.dumps(resp.json(), indent = 1))
    for item in resp.json()['records']:
        if item['name'] == sub_domain:
            id = item['id']
    logging.info('Record ID: %s'% id)
    return id

def updns(idtoken, sub_domain, domain_id, record_id, ip):
    params = dict(
            login_token = idtoken,
            sub_domain = sub_domain,
            domain_id = domain_id,
            record_id = record_id,
            format = 'json',
            record_line='默认',
            value = ip,
            )
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/json', 'User-Agent': 'dnspod-python/0.01 (pzping@gmail.com)'}
    resp = requests.post('https://dnsapi.cn/record.ddns', data = params, headers = headers)
    logging.info('%d %s' % (resp.status_code,resp.reason))
    logging.debug(json.dumps(resp.json(), indent = 1))
    return resp.status_code == 200
    #conn = httplib.HTTPSConnection('dnsapi.cn')
    #conn.request('POST', '/Record.Ddns', urllib.urlencode(params), headers)

    #response = conn.getresponse()
    #print response.status, response.reason
    #data = json.loads(response.read())
    #print json.dumps(data, indent = 1)
    #conn.close()
    #return response.status == 200


def getip():
    sock = socket.create_connection(('ns1.dnspod.net', 6666), 20)
    ip = sock.recv(16)
    sock.close()
    return ip


def main(filename):
    with open(filename,'r') as jfile:
        dconf = json.load(jfile)

    idtoken = '{id},{token}'.format(id = dconf['id'], token = dconf['token'])
    domain = dconf['domain']
    sub_domain = dconf['sub_domain']
    domain_id = getdomainid(idtoken, domain)
    record_id = getrecordid(idtoken, domain_id, sub_domain)
    current_ip = None

    while True:
        try:
            ip = getip()
            logging.info('IP: %s' % ip)
            if current_ip != ip:
                if updns(idtoken, sub_domain, domain_id, record_id, ip):
                    current_ip = ip
                else:
                    logging.info('updnspod error')
        except Exception as e:
            print e
            pass
        time.sleep(60)
    pass



if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        main('./config.json')
