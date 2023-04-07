/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2023-03-17 15:03:07
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-03-31 15:36:13
 * @FilePath: /huanghe/source/services/frontend/mock/service/services/id/event/GET.js
 * @Description: 服务部署事件列表Mock
 */
/* eslint-disable @typescript-eslint/no-var-requires */
const utils = require('../../../../utils');
module.exports = function (req, res) {
  utils.ok(req, res, {
    data: [
      {
        id: 1, // jobId，整数
        status: {
          name: 'warning',
          desc: '异常',
        }, // 状态，字符串，目前两种状态：error（异常｜错误），success（正常）
        name: '作业创建失败', // k8s中事件名称，字符串
        time: '2023-03-15 14:30:00', // 事件产生时间，yyyy-mm-dd hh:mm:ss
      },
      {
        id: 2, // jobId，整数
        status: {
          name: 'error',
          desc: '错误',
        }, // 状态，字符串，目前两种状态：error（异常｜错误），success（正常）
        name: '错误', // k8s中事件名称，字符串
        time: '2023-03-15 14:30:00', // 事件产生时间，yyyy-mm-dd hh:mm:ss
      },
      {
        id: 3, // jobId，整数
        status: {
          name: 'success',
          desc: '成功',
        }, // 状态，字符串，目前两种状态：error（异常｜错误），success（正常）
        name: '作业创建成功', // k8s中事件名称，字符串
        time: '2023-03-15 14:30:00', // 事件产生时间，yyyy-mm-dd hh:mm:ss
      },
      {
        id: 4, // jobId，整数
        status: {
          name: 'success',
          desc: '成功',
        }, // 状态，字符串，目前两种状态：error（异常｜错误），success（正常）
        name: '作业创建成功', // k8s中事件名称，字符串
        time: '2023-03-15 14:30:00', // 事件产生时间，yyyy-mm-dd hh:mm:ss
      },
      {
        id: 5, // jobId，整数
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
