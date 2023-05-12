import os
import tornado

import logging

from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
from tornado.web import StaticFileHandler

from jobmanager import jobManager
from FileExist import FilesEx
import json

jm = jobManager(4, 16)

logging.basicConfig(
    format='%(asctime)s line:%(lineno)s,  %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class MainHandler(RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.render('page/index.html')
class aboutHandler(RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.render('page/about.html')

class jobsHandler(RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

        running_jobs, pending_jobs, finished_jobs, old_jobids = jm.list_jobs()
        
        self.render('page/jobs.html', running_jobs=running_jobs, pending_jobs=pending_jobs, finished_jobs=finished_jobs)
        #self.write('running_jobs:\n' + str(running_jobs) + '\npending_jobs:\n' + str(pending_jobs) +
        #           '\nfinished_jobs:\n' + str(finished_jobs) + 'old_jobs:\n' + str(old_jobids) + '\n')

class StatusHandler(RequestHandler):
    def get(self,id):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        running_jobs_temp, pending_jobs_temp, finished_jobs_temp, old_jobids = jm.list_jobs()
        
        running_jobs = []
        pending_jobs = []
        finished_jobs = []
        for each in running_jobs_temp:
            running_jobs.append(each[0])

        for each in pending_jobs_temp:
            pending_jobs.append(each[0])

        for each in finished_jobs_temp:
            finished_jobs.append(each[0])

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
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        code = 0
        msg = "提交编译失败"
        body_arguments = self.request.body_arguments
        # print(body_arguments.keys())
        id = bytes.decode(body_arguments['inputJobId'][0], encoding='utf-8')
        logger.info("\nCompilingPrjid%s"%id)
        inputFPGA = bytes.decode(
            body_arguments['inputFPGA'][0], encoding='utf-8')
        #XdcFileName = bytes.decode(
            #body_arguments['XdcFileName'][0], encoding='utf-8')
        #inputXdcFile = bytes.decode(
            #body_arguments['inputXdcFile'][0], encoding='utf-8')
        ZipFileName = 'UserZip.zip'
        
        inputZipFile = self.request.files['inputZipFile'][0].get('body')
  #      SrcFileName1 = bytes.decode(
  #          body_arguments['SrcFileName1'][0], encoding='utf-8')
  #      inputFile1 = bytes.decode(
  #          body_arguments['inputFile1'][0], encoding='utf-8')
  #      SrcFileName2 = bytes.decode(
  #          body_arguments['SrcFileName2'][0], encoding='utf-8')
  #      inputFile2 = bytes.decode(
  #          body_arguments['inputFile2'][0], encoding='utf-8')

        #inputFiles = body_arguments['inputFile1']
        # SrcFileName = body_arguments['SrcFilname']
        #print(id, XdcFileName, SrcFileName1, SrcFileName2, inputFPGA)
        # sourcecode = [[XdcFileName, inputXdcFile], [SrcFileName1, inputFile1]]

        sourcecode = [[ZipFileName, inputZipFile]]

        # for i,inputFile in enumerate(inputFiles):
            # sourcecode.append([str(i)+'.v',bytes.decode(inputFile,encoding='utf-8')])

  #      print(sourcecode)
        # if  id and inputFPGA and XdcFileName and inputXdcFile and inputFiles:
        if  id and inputFPGA and inputZipFile:
            code = 1 
            msg = "提交编译成功，请使用查询接口查询编译状态"
        else:
            if not id:
                msg += ",the id is not correct"
            if not inputFPGA:
                msg += ",the inputFPGA is not correct"
            if not inputZipFile:
                msg += ",the inputZipFile is not correct"
            data = {"code": code,"msg": msg}
            self.write(data)
            logger.info("\nCompilingPrjid%sFinish"%id)
            return 

        # if SrcFileName2:
            # sourcecode.append([SrcFileName2, inputFile2])
        data = {"code": code,"msg": msg}
        self.write(data)

        jm.add_a_job(id, sourcecode, inputFPGA, False)
        # self.redirect('/jobs')


class SubmitJSONHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        code = 0
        msg = "提交编译失败"

        # 策略：直接接收一个 JSON string
        body_dict = tornado.escape.json_decode(self.request.body)
        print(body_dict)

        jm.add_a_job(0, body_dict, 'dummy', webcode=False, jsoncode=True)

        code = 1
        msg = "提交编译成功，请使用查询接口查询编译状态"
        data = {"code": code,"msg": msg}
        self.write(data)

    def options(self, *args):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        # no body
        # `*args` is for route with `path arguments` supports
        self.set_status(204)
        self.finish()


class WebcodeHandler(RequestHandler):
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        code = 0
        msg = "提交编译失败"
        body_arguments = self.request.body_arguments
        path = bytes.decode(body_arguments['path'][0], encoding='utf-8')
        logger.info("\nCompilingPrjid%s"%path)
        inputFPGA = "xc7a100tcsg324-1"
        ZipFileName = 'UserZip.zip'
        inputZipFile = ""
        sourcecode = [[ZipFileName, inputZipFile]]
        code = 1 
        msg = "提交编译成功，请使用查询接口查询编译状态"
        
        data = {"code": code,"msg": msg}
        self.write(data)

        jm.add_a_job(path, sourcecode, inputFPGA, True)
        # self.redirect('/jobs')



class QueryHandler(RequestHandler):
    def get(self,id):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        status = 0
        code = 1
        msg = ''
        #output = dict()
        running_jobs_temp, pending_jobs_temp, finished_jobs_temp, old_jobids = jm.list_jobs()

        running_jobs = []
        pending_jobs = []
        finished_jobs = []
        for each in running_jobs_temp:
            running_jobs.append(each[0])

        for each in pending_jobs_temp:
            pending_jobs.append(each[0])

        for each in finished_jobs_temp:
            finished_jobs.append(each[0])
        path = "./jobs/%s/results/top.bit"%id
        file_exist = os.path.exists(path)
        #print(jm.list_jobs())
        if id in running_jobs:
            status = 1
            msg = 'running'
        elif id in pending_jobs:
            status = 2
            msg = 'pending'
        elif (id in finished_jobs or id in old_jobids) and file_exist:
            status = 3
            msg = 'successful'
        elif (id in finished_jobs or id in old_jobids) and ~file_exist:
            status = 4
            with open("./jobs/%s/error.log"%id,'r') as f:
                error = f.read()
            msg = 'compiling failed, the error message is as follows:\n'+error
        else:
            msg = 'error'
            status = 0

        #output["msg"] = msg
        #output["status"] = status
        data = {"code": code,"msg": msg,"data":{"status": status}}
        self.write(data)

class JobListHandler(RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        #output = dict()
        running_jobs_temp, pending_jobs_temp, finished_jobs_temp, old_jobids = jm.list_jobs()

        new_jobs = []
        data = []
        for each in running_jobs_temp:
            data.append([each[0],1,each[1]])
            new_jobs.append(each[0])

        for each in pending_jobs_temp:
            data.append([each[0],2,each[1]])
            new_jobs.append(each[0])

        for each in finished_jobs_temp:
            path = "./jobs/%s/results/top.bit"%each[0]
            file_exist = os.path.exists(path)
            new_jobs.append(each[0])
            if file_exist:
                data.append([each[0],3,each[1]])
            else:
                data.append([each[0],4,each[1]])
            
        for each in old_jobids:
            if each not in new_jobs:
                path = "./jobs/%s/results/top.bit"%each
                file_exist = os.path.exists(path)
                if file_exist:
                    data.append([each,3,""])
                else:
                    data.append([each,4,""])
        self.write({'data':data})

class DownloadHandler(RequestHandler):
    def get(self,id):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        code = 1
        msg = "下载成功"
        path = "./jobs/%s/results/top.bit"%id
        file_exist = os.path.exists(path)
        File_list = FilesEx(id)
        if file_exist:
            data = {"code": code,"msg": msg,"data":File_list}
            self.write(data)
        else:
            code = 0
            msg = "下载失败，没有相应比特流文件"
            data = {"code": code,"msg": msg,"data":File_list}
            self.write(data)

application = tornado.web.Application([
    (r'/submit', SubmitHandler),
    (r'/submit_proj_json', SubmitJSONHandler),
    (r'/jobs', jobsHandler),
    (r'/about', aboutHandler),
    (r'/status/(\w+)',StatusHandler),
    (r'/query/(\w+)',QueryHandler),
    (r'/download/(\w+)',DownloadHandler),
    (r'/api_joblist', JobListHandler),
    (r'/webcode', WebcodeHandler),
    (r"/", MainHandler),
    (r'/(.*)', StaticFileHandler, {'path': './page/'}),
    
])

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(18888)

    logger.info('Server started')
    tornado.ioloop.IOLoop.current().start()
