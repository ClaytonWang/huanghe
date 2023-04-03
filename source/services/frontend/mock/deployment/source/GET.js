/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2023-03-29 14:50:17
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-03-29 14:50:58
 * @FilePath: /huanghe/source/services/frontend/mock/deployment/source/GET.js
 * @Description: 服务部署资源列表Mock
 */
/* eslint-disable @typescript-eslint/no-var-requires */
module.exports = {
  success: true,
  message: '',
  result: {
    data: [
      { name: '1*A100 16C 256G', id: '1' },
      { name: '2*A100 16C 512G', id: '2' },
      { name: '3*A100 24C 768G', id: '3' },
      { name: '4*A100 48C 1024G', id: '4' },
    ],
  },
};
