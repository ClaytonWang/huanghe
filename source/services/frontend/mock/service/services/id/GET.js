/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2023-03-02 15:55:28
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-03-02 15:57:34
 * @FilePath: /frontend/mock/service/services/id/GET.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
module.exports = {
  success: true,
  message: '',
  status: 200,
  result: {
    id: 17,
    status: {
      // 状态
      code: '05',
      name: '',
      desc: '未启动',
    },
    name: 'a17', // 服务名称
    image: {
      // 镜像
      name: 'testname',
      desc: '',
      custom: false,
    },
    source: 'CPU 12C 24G', // 资源配置
    creator: {
      // 创建人
      id: 1,
      username: 'name1',
    },
    project: {
      // 所属项目
      id: 87,
      name: 'shouchen',
    },
    urls: [
      { type: 'public', address: '192.33.23.9' },
      { type: 'private', address: '192.33.23.9' },
    ],
    created_at: '2023-02-03',
    updated_at: '2023-02-03',
    is_public: true, // 公网,布尔类型
  },
};
