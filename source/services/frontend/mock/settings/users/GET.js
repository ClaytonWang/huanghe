/* eslint-disable @typescript-eslint/no-var-requires */
const utils = require('../../utils');
module.exports = function (req, res) {
  utils.list(req, res, {
    data: [
      {
        id: '1', // 列表id，字符串
        username: '张三', // 用户名，字符串
        email: 'san.zhang@digitalbrain.cn', // 用户邮箱，字符串；
        project: {
          // 所属项目，项目对象
          id: 'EN106', // 项目编号，字符串
          name: '紫龙游戏', // 项目名称，字符串
        },
        access: 'edit', // 普通用户权限，可选readonly（只读）｜edit（编辑）
      },
      {
        id: '2', // 列表id，字符串
        username: '张三', // 用户名，字符串
        email: 'san.zhang@digitalbrain.cn', // 用户邮箱，字符串；
        project: {
          // 所属项目，项目对象
          id: 'EN105', // 项目编号，字符串
          name: '足球AI', // 项目名称，字符串
        },
        access: 'edit', // 普通用户权限，可选readonly（只读）｜edit（编辑）
      },
      {
        id: '3', // 列表id，字符串
        username: '李四', // 用户名，字符串
        email: 'si.li@digitalbrain.cn', // 用户邮箱，字符串；
        project: {
          // 所属项目，项目对象
          id: 'EN105', // 项目编号，字符串
          name: '足球AI', // 项目名称，字符串
        },
        access: 'edit', // 普通用户权限，可选readonly（只读）｜edit（编辑）
      },
      {
        id: '4', // 列表id，字符串
        username: '柏栋', // 用户名，字符串
        email: 'baidong.sun@digitalbrain.cn', // 用户邮箱，字符串；
        project: {
          // 所属项目，项目对象
          id: 'EN106', // 项目编号，字符串
          name: '紫龙游戏', // 项目名称，字符串
        },
        access: 'readonly', // 普通用户权限，可选readonly（只读）｜edit（编辑）
      },
      {
        id: '5', // 列表id，字符串
        username: '汪老师', // 用户名，字符串
        email: 'jun.wang@digitalbrain.cn', // 用户邮箱，字符串；
        project: {
          // 所属项目，项目对象
          id: 'EN106', // 项目编号，字符串
          name: '紫龙游戏', // 项目名称，字符串
        },
        access: 'readonly', // 普通用户权限，可选readonly（只读）｜edit（编辑）
      },
      {
        id: '6', // 列表id，字符串
        username: '汪老师', // 用户名，字符串
        email: 'jun.wang@digitalbrain.cn', // 用户邮箱，字符串；
        project: {
          // 所属项目，项目对象
          id: 'EN105', // 项目编号，字符串
          name: '足球AI', // 项目名称，字符串
        },
        access: 'readonly', // 普通用户权限，可选readonly（只读）｜edit（编辑）
      },
    ],
  });
};
