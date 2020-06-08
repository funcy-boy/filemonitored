# -*- coding: UTF-8 -*-
import os
import sys
import json
import time
import socket
import winerror
import requests
import win32event
import win32service
import win32timezone
import servicemanager
import win32serviceutil
from threading import Thread
from configparser import ConfigParser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def push_event(src, time, action):
    ipaddr = socket.gethostbyname(socket.gethostname())
    try:
        post_url = Config['Global'].get('Post_Url')
        requests.post(
            url=post_url,
            timeout=3,
            data={"directory": src,
                  "ipaddres": ipaddr,
                  "time": time,
                  "type": action
                  })

    except requests.exceptions.ConnectTimeout:
        headers = {'Content-Type': 'application/json'}
        bot_url = Config['Global'].get('WechatBot')
        post_data = {
            "msgtype": "markdown",
            "markdown": {
                "content": "filemonitor连接异常：\n >IP地址：<font color='info'> %s </font> \n >发生时间：<font color='warning'> %s </font>" % (ipaddr, time)
            }
        }
        requests.post(url=bot_url,headers=headers,data=json.dumps(post_data))
    

class MyHandler(FileSystemEventHandler):
    
    def on_moved(self, event):
        if event.is_directory:
            pass
        else:
            now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            push_event(event.src_path, now_date, "Moved")

    def on_created(self, event):
        if event.is_directory:
            pass
        else:
            now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            push_event(event.src_path, now_date, "Created")

    def on_deleted(self, event):
        if event.is_directory:
            pass
        else:
            now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            push_event(event.src_path, now_date, "Deleted")

    def on_modified(self, event):
        if event.is_directory:
            pass
        else:
            now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            push_event(event.src_path, now_date, "Modified")


def Monitor(path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


class Monitor_Service(win32serviceutil.ServiceFramework):
    _svc_name_ = 'file_monitor'
    _svc_display_name_ = '站点目录监控服务'
    _svc_description_ = '站点目录监控服务'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.run = True

    def SvcDoRun(self):
        Pathlist = eval(Config['Global'].get('Website_Path'))
        p_list = []
        for Path in Pathlist:
            p = Thread(group=None, target=Monitor, args=(Path,))
            p.start()
            p_list.append(p)
        for p in p_list:
            p.join()
            

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        self.run = False


if __name__ == '__main__':
    Config = ConfigParser()
    Config.read(r'C:\ops\config\config.ini')
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(Monitor_Service)
            servicemanager.Initialize(
                'Monitor_Service', evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            if details == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(Monitor_Service)
