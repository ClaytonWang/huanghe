/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-11-29 10:59:16
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2023-02-28 20:41:35
 * @Description 个人账号接口
 */
const admin = [
  // （一）模块级：后台管理模块
  'bam',
  // （二）页面级：项目列表
  'bam.projects', // 项目模块权限（模块级权限，可以看到最上级导航）
  // （三）按钮级：项目列表页按钮
  'bam.projects.create', // 项目-列表页-「新建项目」按钮权限
  'bam.projects.edit', // 项目-列表页-「编辑」按钮权限
  'bam.projects.delete', // 项目-列表页-「删除」按钮权限

  // （二）页面级：用户列表
  'bam.users', // 项目模块权限（模块级权限，可以看到最上级导航）
  // （三）按钮级：项目列表页按钮
  'bam.users.create', // 项目-列表页-「新建项目」按钮权限
  'bam.users.edit', // 项目-列表页-「编辑」按钮权限
  'bam.users.delete', // 项目-列表页-「删除」按钮权限
];
const owner = [
  // （一）模块级：设置
  'settings',
  // （二）页面级：用户列表页
  'settings.users',
  // （三）按钮级：用户列表页按钮
  'settings.users.create', // 用户-列表页-「新建项目」按钮权限
  'settings.users.edit', // 用户-列表页-「编辑」按钮权限
  'settings.users.delete', // 用户-列表页-「删除」按钮权限

  'storages',
  'storages.list',
  'storages.list.create',
  'storages.list.edit',
  'storages.list.delete',

  'notebooks',
  'notebooks.list',
  'notebooks.list.create',
  'notebooks.list.edit',
  'notebooks.list.delete',

  'jobs',
  'jobs.list',
  'jobs.list.create',
  'jobs.list.edit',
  'jobs.list.delete',

  'services',
  'services.list',
  'services.list.create',
  'services.list.edit',
  'services.list.delete',
];
// const user = [];
const account = {
  success: true,
  message: '',
  result: {
    username: '张三', // 用户名，字符串
    email: 'san.zhang@digitalbrain.cn', // 用户邮箱，字符串
    role: {
      id: 2,
      name: 'admin',
      value: '超级管理员',
    },
    projects: [
      {
        name: '紫龙游戏', // 项目名称，字符串
        id: 'EN106', // 项目编码，字符串
      },
      {
        name: '足球AI', // 项目名称，字符串
        id: 'EN105', // 项目编码，字符串
      },
    ],
    create_at: 'YYYY-MM-DD', // 创建日期，字符串
    permissions: [...admin, ...owner],
  },
};

module.exports = account;
