/**
 * @description 全局属性
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
const APIV1 = '/api/v1';
module.exports = {
  name: '决策智能开发平台',
  footerText: 'Shanghai Digital Brain.Lmt.',
  logo: 'static/logo.svg',
  CORS: [],
  apiPrefix: APIV1,
  apiUriParamsPattern: /:([_a-zA-Z0-9]+)/g,
  api: {
    // login
    login: 'post|/login',
    signup: 'post|/signup',
    logout: 'put|/logout',

    // bam
    bamProjectsList: 'get|/bam/projects',
    bamProjectsCreate: 'post|/bam/projects',
    bamProjectsUpdate: 'put|/bam/projects/:id',
    bamProjectsDelete: 'delete|/bam/projects/:id',
    // bamUsersList: 'get|/bam/users',
    bamUsersList: 'get|/user/users',
    bamUsersCreate: 'post|/bam/users',
    bamUsersUpdate: 'put|/bam/users/:id',
    bamUsersDelete: 'delete|/bam/users/:id',

    // settings
    settingsUsersList: 'get|/settings/users',
    settingsUsersCreate: 'post|/settings/users',
    settingsUsersUpdate: 'put|/settings/users/:id',
    settingsUsersDelete: 'delete|/settings/users/:id',

    settingsUsersPasswordReset: 'post|/users/password/reset',

    settingsAccount: 'get|/account',
    settingsAccountUpdate: 'put|/account/update',
  },
  breadcrumbConfig: {
    '/bam/projects': '项目管理',
    '/bam/users': '用户管理',
    '/settings/users': '用户列表',

    '/settings/account': '我的账号',
  },
  menuItemsConfig: [
    {
      key: 'bam',
      label: '后台管理',
      icon: '',
      children: [
        {
          key: 'bam.projects',
          label: '项目管理',
        },
        {
          key: 'bam.users',
          label: '用户管理',
        },
      ],
    },
    {
      key: 'settings',
      label: '设置',
      icon: '',
      children: [
        {
          key: 'settings.users',
          label: '用户管理',
        },
      ],
    },
  ],
};
