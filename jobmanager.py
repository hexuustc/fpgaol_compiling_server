import os
import queue
import logging
import threading
import shutil

import time
import base64

from compile import compile
from LogExtract import LogEx

JOBS_DIR = 'jobs'

logging.basicConfig(
    format='%(asctime)s line:%(lineno)s,  %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def try_compile(jobdir, id, filenames, device, callback, webcode):
    try:
        compile(jobdir, id, filenames, device, webcode)
    except Exception as e:
        logger.warning('compile got exception %s'%(str(e)))
    callback(id)


class job:
    def _create(self, id, sourcecode, webcode):
        try:
            if os.path.exists(os.path.join(JOBS_DIR, id)):
                shutil.rmtree(os.path.join(JOBS_DIR, id))
            os.mkdir(os.path.join(JOBS_DIR, id))
        except FileExistsError:
            logger.warning('dir (%s) exists' % id)

        self.filenames = []
        if (webcode == False) :
            for filename, code in sourcecode:
                try:
                    f = open(os.path.join(JOBS_DIR, id, filename), 'wb')
                    ZipFileName = 'UserZip.zip'
                    if filename == ZipFileName:
                        #b64_content = base64.urlsafe_b64decode(code)
                        f.write(code)
                    else:
                        f.write(code)
                    f.close()
                    self.filenames.append(filename)
                except Exception as e:
                    logger.warning(
                        'writing sourcecode file (%s) error, value:' % filename, e)

    def __init__(self, id, sourcecode, device, webcode):
        self.id = id
        self.webcode = webcode
        self.submit_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.start_time = '-'
        self.finish_time = '-'
        self.device = device
        self._create(id, sourcecode, webcode)


class jobManager:

    def __init__(self, running_job_max, pending_jobs_max):
        self.running_job_max = running_job_max
        self.running_jobs = dict()
        self.pending_job_max = pending_jobs_max
        self.pending_jobs = queue.Queue(pending_jobs_max)
        self.using_job_id = set()
        self.finished_jobs = []
        self.old_jobs = os.listdir(JOBS_DIR)

        self.lock = threading.Lock()

    def add_a_job(self, id, sourcecode, device, webcode):
        if id in self.using_job_id:
            logger.warning('id(%s) in using' % id)
            return
        self.using_job_id.add(id)
        a_new_job = job(id, sourcecode, device, webcode)
        self.lock.acquire()
        if len(self.running_jobs) < self.running_job_max:
            self.run_a_job(id, a_new_job)
        else:
            self.pend_a_job(id, a_new_job)
        self.lock.release()

    def job_finish(self, id):
        logger.info('job finished %s' % id)
        logger.info("\nCompilingPrjid%sFinish"%id)
        LogEx(id)
        self.lock.acquire()
        self.running_jobs[id].finish_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())
        self.finished_jobs.append(self.running_jobs[id])
        del self.running_jobs[id]
        self.using_job_id.remove(id)
        if not self.pending_jobs.empty():
            job = self.pending_jobs.get()
            self.run_a_job(job.id, job)
        self.lock.release()

    def pend_a_job(self, id, job):
        self.pending_jobs.put(job)

    def run_a_job(self, id, job):
        self.running_jobs[id] = job
        job.start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        threading.Thread(target=try_compile, args=(
            JOBS_DIR, id, job.filenames, job.device, self.job_finish, job.webcode)).start()

    def list_jobs(self):
        ret1 = []
        ret2 = []
        ret3 = []
        self.lock.acquire()
        for id in self.running_jobs:
            job = self.running_jobs[id]
            ret1.append([id, job.submit_time,
                         job.start_time, job.finish_time])
        for job in self.pending_jobs.queue:
            ret2.append([job.id, job.submit_time,
                         job.start_time, job.finish_time])

        for job in self.finished_jobs:
            ret3.append([job.id, job.submit_time,
                         job.start_time, job.finish_time])

        self.lock.release()
        return ret1, ret2, ret3, self.old_jobs
