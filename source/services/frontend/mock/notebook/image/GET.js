/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2023-03-14 10:04:05
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-03-14 10:09:33
 * @FilePath: /huanghe/source/services/frontend/mock/notebook/image/GET.js
 * @Description job image list
 */
/* eslint-disable @typescript-eslint/no-var-requires */
module.exports = {
  success: true,
  message: '',
  result: {
    data: [
      {
        desc: 'xxx', // 镜像描述
        name: 'tensorflow-01',
        id: '1',
      },
      {
        desc: 'xxx', // 镜像描述
        name: 'tensorflow-02',
        id: '2',
      },
    ],
  },
};
