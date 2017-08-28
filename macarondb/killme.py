#!/usr/bin/env python

import sys
import argparse
import templateClass
TC = templateClass.TemplateClass()
TC.sayHi()
import server 
S = server.Server("testDB")
S.sayHi()