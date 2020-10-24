import os
import tornado

import logging

from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
from tornado.web import StaticFileHandler

from jobmanager import jobManager

jm = jobManager(4, 16)

logging.basicConfig(
    format='%(asctime)s line:%(lineno)s,  %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class MainHandler(RequestHandler):
    def get(self):
        self.render('page/index.html')
class aboutHandler(RequestHandler):
    def get(self):
        self.render('page/about.html')

class jobsHandler(RequestHandler):
    def get(self):

        running_jobs, pending_jobs, finished_jobs, old_jobids = jm.list_jobs()
        
        self.render('page/jobs.html', running_jobs=running_jobs, pending_jobs=pending_jobs, finished_jobs=finished_jobs)
        #self.write('running_jobs:\n' + str(running_jobs) + '\npending_jobs:\n' + str(pending_jobs) +
        #           '\nfinished_jobs:\n' + str(finished_jobs) + 'old_jobs:\n' + str(old_jobids) + '\n')

class StatusHandler(RequestHandler):
    def get(self,id):
        running_jobs, pending_jobs, finished_jobs, old_jobids = jm.list_jobs()
        if id in running_jobs:
            self.write('running')
        elif id in pending_jobs:
            self.write('pending')
        elif id in finished_jobs or id in old_jobids:
            self.write('finished')
        else:
            self.write('error')


class SubmitHandler(RequestHandler):
    def post(self):
        body_arguments = self.request.body_arguments
        # print(body_arguments.keys())
        id = bytes.decode(body_arguments['inputJobId'][0], encoding='utf-8')
        inputFPGA = bytes.decode(
            body_arguments['inputFPGA'][0], encoding='utf-8')
        XdcFileName = bytes.decode(
            body_arguments['XdcFileName'][0], encoding='utf-8')
        inputXdcFile = bytes.decode(
            body_arguments['inputXdcFile'][0], encoding='utf-8')
        SrcFileName1 = bytes.decode(
            body_arguments['SrcFileName1'][0], encoding='utf-8')
        inputFile1 = bytes.decode(
            body_arguments['inputFile1'][0], encoding='utf-8')
        SrcFileName2 = bytes.decode(
            body_arguments['SrcFileName2'][0], encoding='utf-8')
        inputFile2 = bytes.decode(
            body_arguments['inputFile2'][0], encoding='utf-8')
        #print(id, XdcFileName, SrcFileName1, SrcFileName2, inputFPGA)
        sourcecode = [[XdcFileName, inputXdcFile], [SrcFileName1, inputFile1]]
        if SrcFileName2:
            sourcecode.append([SrcFileName2, inputFile2])
        jm.add_a_job(id, sourcecode, inputFPGA)
        self.redirect('/jobs')


application = tornado.web.Application([
    (r'/submit', SubmitHandler),
    (r'/jobs', jobsHandler),
    (r'/about', aboutHandler),
    (r'/status/(\w+)',StatusHandler),
    (r"/", MainHandler),
    (r'/(.*)', StaticFileHandler, {'path': './page/'}),
])

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)

    logger.info('Server started')
    tornado.ioloop.IOLoop.current().start()
