/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2023-02-27 10:32:46
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-03-20 10:15:21
 * @FilePath: /huanghe/source/services/frontend/mock/notebook/notebooks/id/GET.js
 * @Description: Notebook详情
 */
/* eslint-disable @typescript-eslint/no-var-requires */
/* eslint-disable max-len */
const utils = require('../../../utils');
module.exports = function (req, res) {
  utils.ok(req, res, {
    id: 86,
    name: 'pv3create',
    creator: {
      id: 1,
      username: 'name1',
    },
    created_at: '2023-03-13T20:20:40.259598',
    status: {
      code: '05',
      name: 'stopped',
      desc: '已停止',
    },
    url: null,
    project: {
      id: 100,
      name: '测试0306',
    },
    image: {
      name: 'swr.cn-north-4.myhuaweicloud.com/digitalbrain/codeserver-java:v0.1',
      desc: '',
      custom: false,
    },
    source: 'CPU 1C 1G',
    hooks: [
      {
        storage: {
          name: 'test1',
          id: 39,
        },
        path: '/home/jovyan',
      },
    ],
    updated_at: '2023-03-13T20:20:40.259598',
    grafana: {
      cpu: 'https://grafana.digitalbrain.cn:32443/d-solo/3JLLppA4k/notebookjian-kong?orgId=1&var-namespace=dev-cs0306test0306&var-cluster=&var-job=admin-pv3create-0&panelId=4&from=1678784276663&to=1678787760521',
      ram: 'https://grafana.digitalbrain.cn:32443/d-solo/3JLLppA4k/notebookjian-kong?orgId=1&var-namespace=dev-cs0306test0306&var-cluster=&var-job=admin-pv3create-0&panelId=6&from=1678784276663&to=1678787760521',
      gpu: '',
      vram: '',
    },
    server_ip: null,
    ssh: {
      account: 'jovyan',
      password: 'jovyan',
      address: null,
    },
  });
};
