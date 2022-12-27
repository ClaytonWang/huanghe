/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-12-27 10:52:36
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-27 11:00:07
 * @Description Notebook详情
 */
/* eslint-disable @typescript-eslint/no-var-requires */
const utils = require('../../utils');
module.exports = function (req, res) {
  utils.ok(req, res, {
    id: '1', // notebookId，字符串
    name: 'hb-test-01', // 名称，字符串，仅支持英文名称
    project: 'ENG106', // projectId, string
    image: '1', // imageId, string
    source: '1', // 资源Id，字符串
    hooks: [
      {
        storage: '1', // 存储盘Id, 字符串
        path: '/home/jovyan/vol-1', // 目录，字符串，前端校验需符合文件路径格式
      },
      {
        storage: '2', // 存储盘Id, 字符串
        path: '/home/jovyan/vol-2', // 目录，字符串，前端校验需符合文件路径格式
      },
    ],
  });
};
