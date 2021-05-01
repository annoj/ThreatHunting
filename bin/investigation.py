#!/usr/bin/env python3

import sys
import os
import time
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from splunklib.searchcommands import dispatch
from splunklib.searchcommands import GeneratingCommand
from splunklib.searchcommands import Configuration
from splunklib.searchcommands import Option
from splunklib.searchcommands import validators

@Configuration()
class GenerateInvestigationCommand(GeneratingCommand):
    parent_uuid = Option(require=False)
    root = Option(require=True, validate=validators.Boolean())
    header = Option(require=False)
    body = Option(require=True)
    author = Option(require=True)
    def generate(self):
        if not self.root and not self.parent_uuid:
            raise Exception('Child node must have parent_uuid!')
        yield {
                '_time': time.time(),
                '_raw': (  
                          f'uuid: {str(uuid.uuid4())} '
                        + f'parent_uuid: {self.parent_uuid} '
                        + f'author: {self.author} '
                        + f'header: {self.header} '
                        + f'body: {self.body}'
                )
        }

dispatch(GenerateInvestigationCommand, sys.argv, sys.stdin, sys.stdout, __name__)
