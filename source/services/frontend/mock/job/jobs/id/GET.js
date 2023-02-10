/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-12-27 10:52:36
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-27 11:00:07
 * @Description Notebook详情
 */
/* eslint-disable @typescript-eslint/no-var-requires */
const utils = require('../../../utils');
module.exports = function (req, res) {
  utils.ok(req, res, {
    success: true,
    message: '',
    status: 200,
    result: {
      id: 1,
      name: 'a7',
      creator: {
        id: '1',
        username: 'name1',
      },
      created_at: '2023-02-03',
      status: {
        code: '05',
        name: 'stopped',
        desc: '已停止',
      },
      project: {
        id: '87',
        name: 'shouchen',
      },
      image: {
        name: 'testname',
        custom: false,
      },
      source: 'CPU 12C 24G',
      hooks: [
        {
          storage: {
            name: 'shouchen',
            id: 27,
          },
          path: '/home/jovyan',
        },
      ],
      updated_at: '2023-02-03',
      mode: '调试',
    },
  });
};
