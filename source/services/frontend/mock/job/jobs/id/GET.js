/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2023-02-27 10:32:46
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-03-16 14:28:54
 * @FilePath: /huanghe/source/services/frontend/mock/job/jobs/id/GET.js
 * @Description: Notebook详情
 */
/* eslint-disable @typescript-eslint/no-var-requires */
/* eslint-disable max-len */
const utils = require('../../../utils');
module.exports = function (req, res) {
  utils.ok(req, res, {
    id: 62,
    name: 'newjob',
    creator: {
      id: '1',
      username: 'name1',
    },
    created_at: '2023-03-14',
    status: {
      code: '03',
      name: 'pending',
      desc: '排队中',
    },
    project: {
      id: 100,
      name: '测试0306',
    },
    image: {
      name: 'swr.cn-north-4.myhuaweicloud.com/digitalbrain/codeserver-java:v0.1',
      custom: false,
    },
    source: 'CPU 1C 1G',
    hooks: [
      {
        storage: {
          name: 'sd22',
          id: 28,
        },
        path: '/home/jovyan/vol-1',
      },
      {
        storage: {
          name: 'sd33',
          id: 29,
        },
        path: '/home/jovyan/vol-1',
      },
    ],
    updated_at: '2023-03-14',
    mode: '调试',
    url: 'http://121.36.41.231:31767/?arg=-ndev-cs0306test0306&arg=admin-newjob-tfjob-0&arg=bash',
    grafana: {
      cpu: 'https://grafana.digitalbrain.cn:32443/d-solo/3JLLppA4k/notebookjian-kong?orgId=1&var-namespace=dev-cs0306test0306&var-cluster=&var-job=admin-newjob-tfjob-0&panelId=4&from=1678784276663&to=1678787760521',
      ram: 'https://grafana.digitalbrain.cn:32443/d-solo/3JLLppA4k/notebookjian-kong?orgId=1&var-namespace=dev-cs0306test0306&var-cluster=&var-job=admin-newjob-tfjob-0&panelId=6&from=1678784276663&to=1678787760521',
      gpu: '',
      vram: '',
    },
    logging_url:
      'https://grafana.digitalbrain.cn:32443/d/o6-BGgnnk/kubernetes-logs?orgId=1&theme=light&viewPanel=2&var-namespace=dev-cs0306test0306&var-app=admin-newjob',
    start_command: 'sleep 14400',
    work_dir: 'stella',
    start_mode: {
      id: 1,
      name: '单机',
    }, // 启动方式id，整数
    nodes: 2, // 节点数，整数
  });
};
