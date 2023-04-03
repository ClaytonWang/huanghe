/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2023-03-14 20:49:23
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-03-14 22:51:38
 * @FilePath: /huanghe/source/services/frontend/mock/monitor/servers/GET.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
/* eslint-disable @typescript-eslint/no-var-requires */
const utils = require('../../utils');
module.exports = function (req, res) {
  utils.ok(req, res, {
    data: [
      {
        id: 134,
        status: 'Success',
        server: '172.16.0.86',
        occupied_rate: 0.9,
        source: 'GPU 2*T4 16C 62G',
        occupied_by: [],
      },
      {
        id: 133,
        status: 'Success',
        server: '172.16.0.55',
        occupied_rate: 0.7,
        source: 'CPU 16C 31G',
        occupied_by: [],
      },
      {
        id: 132,
        status: 'Success',
        server: '172.16.0.240',
        occupied_rate: 0.07,
        source: 'CPU 16C 15G',
        occupied_by: [
          {
            id: 1,
            username: 'test',
            tasks: [
              {
                name: 'testssss',
                source: 'CPU 1C 1G',
              },
            ],
          },
        ],
      },
      {
        id: 132,
        status: 'Success',
        server: '172.16.0.240',
        occupied_rate: 0.5,
        source: 'CPU 16C 15G',
        occupied_by: [
          {
            id: 1,
            username: 'test',
            tasks: [
              {
                name: 'testssss',
                source: 'CPU 1C 1G',
              },
            ],
          },
        ],
      },
    ],
    total: 3,
    pageno: 1,
    pagesize: 10,
  });
};
