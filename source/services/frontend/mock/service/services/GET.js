/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-12-14 19:58:57
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-14 20:04:11
 * @Description Notebook列表
 */
/* eslint-disable @typescript-eslint/no-var-requires */
const utils = require('../../utils');
module.exports = function (req, res) {
  utils.list(req, res, {
    data: [
      {
        id: 17,
        status: {
          // 状态
          code: '05',
          name: 'stopped',
          desc: '已停止',
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
          { type: 'public', address: '127.39.43.25' },
          { type: 'private', address: '195.39.43.25' },
        ],
        created_at: '2023-02-03',
        updated_at: '2023-02-03',
        is_public: true, // 公网,布尔类型
      },
      {
        id: 18,
        status: {
          // 状态
          code: '06',
          name: 'start',
          desc: '启动中',
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
          { type: 'public', address: '127.39.43.25' },
          { type: 'private', address: '195.39.43.25' },
        ],
        created_at: '2023-02-03',
        updated_at: '2023-02-03',
        is_public: true, // 公网,布尔类型
      },
      {
        id: 19,
        status: {
          // 状态
          code: '07',
          name: 'running',
          desc: '已启动',
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
          { type: 'public', address: '127.39.43.25' },
          { type: 'private', address: '195.39.43.25' },
        ],
        created_at: '2023-02-03',
        updated_at: '2023-02-03',
        is_public: true, // 公网,布尔类型
      },
      {
        id: 20,
        status: {
          // 状态
          code: '08',
          name: 'error',
          desc: '启动失败',
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
          { type: 'public', address: '127.39.43.25' },
          { type: 'private', address: '195.39.43.25' },
        ],
        created_at: '2023-02-03',
        updated_at: '2023-02-03',
        is_public: true, // 公网,布尔类型
      },
      {
        id: 21,
        status: {
          // 状态
          code: '05',
          name: 'stop',
          desc: '停止中',
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
          { type: 'public', address: '127.39.43.25' },
          { type: 'private', address: '195.39.43.25' },
        ],
        created_at: '2023-02-03',
        updated_at: '2023-02-03',
        is_public: true, // 公网,布尔类型
      },
      {
        id: 22,
        status: {
          // 状态
          code: '05',
          name: 'pending',
          desc: '排队中',
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
        urls: [{ type: 'private', address: '195.39.43.25' }],
        created_at: '2023-02-03',
        updated_at: '2023-02-03',
        is_public: false, // 公网,布尔类型
      },
    ],
  });
};
