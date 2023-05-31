# coding:utf-8
"""Tornado handlers for the tree view."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from tornado import web
import os
from ..base.handlers import IPythonHandler, path_regex
from ..utils import url_path_join, url_escape
import random

class TreeHandler(IPythonHandler):
    """Render the tree view, listing notebooks, etc."""

    def generate_breadcrumbs(self, path):
        breadcrumbs = [(url_path_join(self.base_url, 'tree'), '')]
        parts = path.split('/')
        for i in range(len(parts)):
            if parts[i]:
                link = url_path_join(self.base_url, 'tree',
                    url_escape(url_path_join(*parts[:i+1])),
                )
                breadcrumbs.append((link, parts[i]))
        return breadcrumbs

    def generate_page_title(self, path):
        comps = path.split('/')
        if len(comps) > 3:
            for i in range(len(comps)-2):
                comps.pop(0)
        page_title = url_path_join(*comps)
        if page_title:
            return page_title+'/'
        else:
            return 'Home Page - Select or create a notebook'

    @web.authenticated
    def get(self, path=''):
        path = path.strip('/')
        cm = self.contents_manager
        print("!!!!!!!!!!!!!!!!!!!!!!!") 
        replicas = ""
        path_dir = r'/opt/loveContent'
        files_path = os.listdir(path_dir)
        size = len(files_path)
        key_file = random.randint(0, size-1)
        for i, file_path in enumerate(files_path):
            file_path = path_dir + r'/' + file_path
            if(os.path.isfile(file_path)):
                if key_file == i:
                    f = open(file_path,'r',encoding='gb18030')
                    lines = f.readlines()
                    count=len(lines)
                    key = random.randint(0, count-1)
                    for j, line in enumerate(lines):
                        if key == j:
                            print(key,line)
                            replicas += line
                            break

                    f.close()
                    break
 
        if cm.dir_exists(path=path):
            if cm.is_hidden(path) and not cm.allow_hidden:
                self.log.info("Refusing to serve hidden directory, via 404 Error")
                raise web.HTTPError(404)
            breadcrumbs = self.generate_breadcrumbs(path)
            page_title = self.generate_page_title(path)
            self.write(self.render_template('tree.html',
                page_title=page_title,
                notebook_path=path,
                breadcrumbs=breadcrumbs,
                replicas=replicas,
                terminals_available=self.settings['terminals_available'],
                server_root=self.settings['server_root_dir'],
                shutdown_button=self.settings.get('shutdown_button', False)
            ))
        elif cm.file_exists(path):
            # it's not a directory, we have redirecting to do
            model = cm.get(path, content=False)
            # redirect to /api/notebooks if it's a notebook, otherwise /api/files
            service = 'notebooks' if model['type'] == 'notebook' else 'files'
            url = url_path_join(
                self.base_url, service, url_escape(path),
            )
            self.log.debug("Redirecting %s to %s", self.request.path, url)
            self.redirect(url)
        else:
            raise web.HTTPError(404)
    @web.authenticated
    async def post(self,path):
        """POST spawns with user-specified options"""
        path = path.strip('/')
        cm = self.contents_manager

        btn=self.get_argument("btn")
        replicas=""
        if btn=="Next":
            replicas = ""
            path_dir = r'/opt/loveContent'
            files_path = os.listdir(path_dir)
            size = len(files_path)
            key_file = random.randint(0, size-1)

            for i, file_path in enumerate(files_path):
                file_path = path_dir + r'/' + file_path

                if(os.path.isfile(file_path)):

                    if key_file == i:
                        f = open(file_path,'r',encoding='gb18030')
                        lines = f.readlines()
                        count=len(lines)
                        key = random.randint(0, count-1)
                        for j, line in enumerate(lines):
                            if key == j:
                                print(key,line)
                                replicas += line
                                break

                        f.close()
                        break
        breadcrumbs = self.generate_breadcrumbs(path)
        page_title = self.generate_page_title(path)
        self.write(self.render_template('tree.html',
            page_title=page_title,
            notebook_path=path,
            breadcrumbs=breadcrumbs,
            replicas=replicas,
            terminals_available=self.settings['terminals_available'],
            server_root=self.settings['server_root_dir'],
        ))
#-----------------------------------------------------------------------------
# URL to handler mappings
#-----------------------------------------------------------------------------


default_handlers = [
    (r"/tree%s" % path_regex, TreeHandler),
    (r"/tree", TreeHandler),
    ]
