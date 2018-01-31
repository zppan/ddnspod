#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import sys
import httplib
import urllib
import socket
import requests
import time
import json
import logging

logging.basicConfig(level=logging.INFO)

# Use Token, check https://support.dnspod.cn/Kb/showarticle/tsid/227/

current_ip = None

class DDnspod(object):
    def __init__(self, idtoken, sub_domain):
        self.idtoken = idtoken
        self.sub_domain = sub_domain
        self.headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json", "User-Agent": "dnspod-python/0.01 (pzping@gmail.com)"}
        self.domain_id = self.getdomainid()
        self.record_id = self.getrecordid()

    def getdomainid(self):
        params = dict(
                login_token = self.idtoken,
                format = "json",
                )
        resp = requests.post("https://dnsapi.cn/domain.list", data = params, headers = self.headers)
        id = resp.json()["domains"][0]["id"]
        logging.info("Domain ID: %s"% id)
        return id

    def getrecordid(self):
        params = dict(
                login_token = self.idtoken,
                sub_domain = self.sub_domain,
                domain_id = self.domain_id,
                format = "json",
                )
        resp = requests.post("https://dnsapi.cn/record.list", data = params, headers = self.headers)
        id = resp.json()["records"][0]["id"]
        logging.info("Record ID: %s"% id)
        return id

    def updns(self, ip):
        params = dict(
                login_token = self.idtoken,
                sub_domain = self.sub_domain,
                domain_id = self.domain_id,
                record_id = self.record_id,
                format = "json",
                record_line="默认",
                value = ip,
                )
        resp = requests.post("https://dnsapi.cn/record.ddns", data = params, headers = self.headers)
        logging.info("%d %s" % (resp.status_code,resp.reason))
        print json.dumps(resp.json(), indent = 1)
        return resp.status_code == 200
        #conn = httplib.HTTPSConnection("dnsapi.cn")
        #conn.request("POST", "/Record.Ddns", urllib.urlencode(params), self.headers)

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

def getIDToken(filename = "./dnspodToken.json"):
    with open(filename,"r") as jfile:
        tken = json.load(jfile)
        return "%s,%s" % (tken["ID"],tken["Token"])

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        ddns = DDnspod(getIDToken(sys.argv[1]),"pi")
    else:
        ddns = DDnspod(getIDToken(),"pi")
    while True:
        try:
            ip = getip()
            logging.info("IP: %s" % ip)
            if current_ip != ip:
                if ddns.updns(ip):
                    current_ip = ip
                else:
                    logging.info("updnspod error")
        except Exception as e:
            print e
            pass
        time.sleep(60)

