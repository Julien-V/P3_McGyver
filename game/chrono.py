#!/usr/bin/python3
# coding : utf-8

from datetime import datetime


class Chrono(object):
    def __init__(self):
        self.chrono = datetime.now()
        self.paused_seconds = 0
        self.started = True

    def pause(self):
        if self.started:
            self.pause_t = datetime.now()
            self.started = False

    def resume(self):
        if not self.started:
            self.paused_seconds += (datetime.now()-self.pause_t).seconds
            self.started = True

    def get_chrono(self):
        if self.started:
            return (datetime.now()-self.chrono).seconds-self.paused_seconds
        else:
            return (self.pause_t-self.chrono).seconds-self.paused_seconds
