/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-11-29 12:19:26
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-05 18:09:37
 * @Description 项目负责人可见的设置模块-用户里诶博啊
 */
/* eslint-disable @typescript-eslint/no-var-requires */
const utils = require('../../utils');
module.exports = function (req, res) {
  utils.list(req, res, {
    data: [
      {
        id: 1,
        username: '更新用户名',
        email: 'admin@163.com',
        project: {
          id: 5,
          code: '002321',
          name: '数据标注2',
        },
        permissions: [
          {
            id: 31,
            name: 'edit',
            value: '编辑',
            code: '00030002',
          },
        ],
      },
      {
        id: 2,
        username: '更新用户名',
        email: 'admin@163.com',
        project: {
          id: 5,
          code: '002321',
          name: '数据标注2',
        },
        permissions: [
          {
            id: 31,
            name: 'edit',
            value: '编辑',
            code: '00030002',
          },
        ],
      },
      {
        id: 3,
        username: '更新用户名',
        email: 'admin@163.com',
        project: {
          id: 5,
          code: '002321',
          name: '数据标注2',
        },
        permissions: [
          {
            id: 30,
            name: 'readonly',
            value: '查看',
            code: '00030001',
          },
        ],
      },
    ],
  });
};
