/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2023-03-15 10:41:29
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-03-15 11:07:01
 * @FilePath: /huanghe/source/services/frontend/mock/job/startmodes/GET.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
/* eslint-disable @typescript-eslint/no-var-requires */
const utils = require('../../utils');
module.exports = function (req, res) {
  utils.ok(req, res, [
    {
      id: 1,
      name: '单机',
      max_nodes: 1,
    },
    {
      id: 2,
      name: '分布式：MPI',
      max_nodes: 2,
    },
    {
      id: 3,
      name: '分布式：DeepSpeed',
      max_nodes: 2,
    },
  ]);
};
