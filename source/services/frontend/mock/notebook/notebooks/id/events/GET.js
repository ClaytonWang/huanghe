/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2023-03-20 10:24:57
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-03-20 10:27:01
 * @FilePath: /huanghe/source/services/frontend/mock/notebook/notebooks/id/events/GET.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
/* eslint-disable @typescript-eslint/no-var-requires */
const utils = require('../../../../utils');
module.exports = function (req, res) {
  utils.ok(req, res, {
    data: [
      {
        id: 1,
        status: {
          name: 'warning',
          desc: '异常',
        }, // 状态，字符串，目前两种状态：error（异常｜错误），success（正常）
        name: '作业创建失败', // k8s中事件名称，字符串
        time: '2023-03-15 14:30:00', // 事件产生时间，yyyy-mm-dd hh:mm:ss
      },
      {
        id: 2,
        status: {
          name: 'error',
          desc: '错误',
        }, // 状态，字符串，目前两种状态：error（异常｜错误），success（正常）
        name: '错误', // k8s中事件名称，字符串
        time: '2023-03-15 14:30:00', // 事件产生时间，yyyy-mm-dd hh:mm:ss
      },
      {
        id: 3,
        status: {
          name: 'success',
          desc: '成功',
        }, // 状态，字符串，目前两种状态：error（异常｜错误），success（正常）
        name: '作业创建成功', // k8s中事件名称，字符串
        time: '2023-03-15 14:30:00', // 事件产生时间，yyyy-mm-dd hh:mm:ss
      },
      {
        id: 4,
        status: {
          name: 'success',
          desc: '成功',
        }, // 状态，字符串，目前两种状态：error（异常｜错误），success（正常）
        name: '作业创建成功', // k8s中事件名称，字符串
        time: '2023-03-15 14:30:00', // 事件产生时间，yyyy-mm-dd hh:mm:ss
      },
      {
        id: 5,
        status: {
          name: 'success',
          desc: '成功',
        }, // 状态，字符串，目前两种状态：error（异常｜错误），success（正常）
        name: '作业创建成功', // k8s中事件名称，字符串
        time: '2023-03-15 14:30:00', // 事件产生时间，yyyy-mm-dd hh:mm:ss
      },
    ],
    total: 10,
    pageno: 1,
    pagesize: 2,
  });
};
