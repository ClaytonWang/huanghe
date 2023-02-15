/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-12-14 19:58:57
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-14 20:04:11
 * @Description Notebook列表
 */
/* eslint-disable @typescript-eslint/no-var-requires */
const utils = require('../utils');
module.exports = function (req, res) {
  utils.list(req, res, {
    data: [
      {
        id: 1,
        status: 'success', // 状态，字符串，包括success（正常）｜error（异常）
        server: '192.33.20.24', // server IP, 字符串
        occupied_rate: '1/2', // 占用率，字符串，分数
        source: 'CPU 12C 24G', // 资源配置，字符串
        occupied_by: [
          // 占用人，对象数组
          { id: 1, username: '张三' }, // 用户id和用户名
          { id: 2, username: '李四' },
        ],
      },
    ],
  });
};
