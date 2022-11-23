/**
 * @description Mock：计划列表
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
/* eslint-disable @typescript-eslint/no-var-requires */
const utils = require('../../utils');
module.exports = function (req, res) {
  utils.list(req, res, {
    data: [
      {
        id: 'ENG105', // 项目ID，字符串
        code: 'ENG105', // 项目编码，字符串。
        name: '足球AI', // 项目名称，字符串
        owner: '田老师', // 项目负责人姓名，字符串
        createDate: '2022-10-10', // 创建时间,字符串
      },
      {
        id: 'ENG106', // 项目ID，字符串
        code: 'ENG106', // 项目编码,字符串。
        name: '紫龙游戏', // 项目名称,字符串
        owner: '田老师', // 项目负责人姓名,字符串
        createDate: '2022-10-10', // 创建时间,字符串
      },
      {
        id: 'ENG112', // 项目ID，字符串
        code: 'ENG112', // 项目编码,字符串。
        name: '运筹', // 项目名称,字符串
        owner: '张伟楠', // 项目负责人姓名,字符串
        createDate: '2022-10-10', // 创建时间,字符串
      },
      {
        id: 'ENG113', // 项目ID，字符串
        code: 'ENG113', // 项目编码,字符串。
        name: '大模型', // 项目名称,字符串
        owner: '温颖', // 项目负责人姓名,字符串
        createDate: '2022-10-10', // 创建时间,字符串
      },
      {
        id: 'ENG114', // 项目ID，字符串
        code: 'ENG114', // 项目编码,字符串。
        name: 'AI bot', // 项目名称,字符串
        owner: '田老师', // 项目负责人姓名,字符串
        createDate: '2022-10-10', // 创建时间，字符串
      },
    ],
  });
};
