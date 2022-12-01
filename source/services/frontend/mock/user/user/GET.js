/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-11-29 12:19:26
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-01 09:59:43
 * @Description 后台管理：用户列表查询
 */
/* eslint-disable @typescript-eslint/no-var-requires */
const utils = require('../../utils');
module.exports = function (req, res) {
  utils.list(req, res, {
    data: [
      {
        id: '', //
        username: '刘龙飞', // 用户名,字符串
        email: 'longfei.liu@digitalbrain.cn', // 用户邮箱,字符串；
        role: 'admin', // 角色,可选admin｜owner｜user,字符串
        project: [], // 所属项目名称,数组
        create_at: '2022-10-10', // 创建时间,字符串
      },
      {
        username: '田政', // 用户名,字符串
        email: 'zheng.tian@digitalbrain.cn', // 用户邮箱,字符串；
        role: 'owner', // 角色,可选admin｜owner｜user,字符串
        project: [
          // 所属项目名称,项目对象数组
          {
            id: 'EN106',
            name: '紫龙游戏',
          },
        ],
        create_at: '2022-10-10', // 创建时间,字符串
      },
      {
        username: '温颖', // 用户名,字符串
        email: 'ying@digitalbrain.cn', // 用户邮箱,字符串；
        role: 'owner', // 角色,可选admin｜owner｜user,字符串
        project: [
          // 所属项目名称,项目对象数组
          {
            id: 'EN107',
            name: '大模型',
          },
        ],
        create_at: '2022-10-10', // 创建时间,字符串
      },
      {
        username: '张伟楠', // 用户名,字符串
        email: 'weinan@digitalbrain.cn', // 用户邮箱,字符串；
        role: 'owner', // 角色,可选admin｜owner｜user,字符串
        project: [
          // 所属项目名称,项目对象数组
          {
            id: 'EN108',
            name: '运筹',
          },
        ],
        create_at: '2022-10-10', // 创建时间,字符串
      },
      {
        username: '张三', // 用户名,字符串
        email: 'san@digitalbrain.cn', // 用户邮箱,字符串；
        role: 'user', // 角色,可选admin｜owner｜user,字符串
        project: [
          // 所属项目名称,项目对象数组
          {
            id: 'EN106',
            name: '紫龙游戏',
          },
          {
            id: 'EN107',
            name: '大模型',
          },
        ],
        create_at: '2022-10-10', // 创建时间,字符串
      },
      {
        username: '李四', // 用户名,字符串
        email: 'si@digitalbrain.cn', // 用户邮箱,字符串；
        role: 'user', // 角色,可选admin｜owner｜user,字符串
        project: [
          // 所属项目名称,项目对象数组
          {
            id: 'EN107',
            name: '大模型',
          },
          {
            id: 'EN108',
            name: '运筹',
          },
        ],
        create_at: '2022-10-10', // 创建时间,字符串
      },
    ],
  });
};
