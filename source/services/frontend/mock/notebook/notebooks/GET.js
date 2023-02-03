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
        id: '1', // notebookId，字符串
        status: {
          code: '', // 状态码，字符串
          name: 'stopped', // 状态名称，stopped｜pending｜error｜running
          desc: '停止', // 状态描述，字符串
        }, // 状态
        name: 'hb-test-01', // 名称，字符串，仅支持英文名称
        project: {
          name: '紫龙游戏', // 项目名称，字符串
          id: 'EN106', // 项目ID，字符串
        }, // 所属项目
        image: {
          name: 'kubeflownotebook01', // 镜像，字符串
          desc: '', // 镜像描述，字符串
        },
        source: '1*A100 8C 32G', // 资源，字符串
        creator: {
          id: '1', // 用户ID，字符串
          username: 'name1', // 用户名称，字符串
        }, // 创建人
        created_at: '2022-09-03', // 创建时间，字符串
      },
      {
        id: '2', // notebookId，字符串
        status: {
          code: '', // 状态码，字符串
          name: 'pending', // 状态名称，stopped｜pending｜error｜running
          desc: '启动中', // 状态描述，字符串
        }, // 状态
        name: 'hb-test-02', // 名称，字符串，仅支持英文名称
        project: {
          name: '紫龙游戏', // 项目名称，字符串
          id: 'EN106', // 项目ID，字符串
        }, // 所属项目
        image: {
          name: 'kubeflownotebook01', // 镜像，字符串
          desc: '', // 镜像描述，字符串
        },
        source: '1*A100 8C 32G', // 资源，字符串
        creator: {
          id: '2', // 用户ID，字符串
          username: '温老师', // 用户名称，字符串
        }, // 创建人
        created_at: '2022-10-03', // 创建时间，字符串
      },
      {
        id: '3', // notebookId，字符串
        status: {
          code: '', // 状态码，字符串
          name: 'error', // 状态名称，stopped｜pending｜error｜running
          desc: '内存不足，需要排队', // 状态描述，字符串
        }, // 状态
        name: 'hb-test-03', // 名称，字符串，仅支持英文名称
        project: {
          name: '紫龙游戏', // 项目名称，字符串
          id: 'EN106', // 项目ID，字符串
        }, // 所属项目
        image: {
          name: 'kubeflownotebook01', // 镜像，字符串
          desc: '', // 镜像描述，字符串
        },
        source: '1*A100 8C 32G', // 资源，字符串
        creator: {
          id: '3', // 用户ID，字符串
          username: '大张伟老师', // 用户名称，字符串
        }, // 创建人
        created_at: '2022-11-03', // 创建时间，字符串
      },
      {
        id: '4', // notebookId，字符串
        status: {
          code: '', // 状态码，字符串
          name: 'running', // 状态名称，stopped｜pending｜error｜running
          desc: '运行中', // 状态描述，字符串
        }, // 状态
        name: 'hb-test-03', // 名称，字符串，仅支持英文名称
        project: {
          name: '紫龙游戏', // 项目名称，字符串
          id: 'EN106', // 项目ID，字符串
        }, // 所属项目
        image: {
          name: 'kubeflownotebook01', // 镜像，字符串
          desc: '', // 镜像描述，字符串
        },
        source: '1*A100 8C 32G', // 资源，字符串
        creator: {
          id: '3', // 用户ID，字符串
          username: '大张伟老师', // 用户名称，字符串
        }, // 创建人
        created_at: '2022-11-03', // 创建时间，字符串
      },
    ],
  });
};
