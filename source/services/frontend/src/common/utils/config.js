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
    login: 'post|/user/auth/login',
    logout: 'put|/user/auth/logout',

    // bam
    bamProjectsList: 'get|/user/project',
    bamProjectsCreate: 'post|/user/project',
    bamProjectsUpdate: 'put|/user/project/:project_id',
    bamProjectsDelete: 'delete|/user/project/:project_id',
    // bamUsersList: 'get|/bam/users',
    bamUsersList: 'get|/user/user',
    bamUsersCreate: 'post|/user/user',
    bamUsersUpdate: 'put|/user/user/:user_id',
    bamUsersDelete: 'delete|/user/user/:user_id',

    // settings
    settingsUsersList: 'get|/settings/users',
    settingsUsersCreate: 'post|/settings/users',
    settingsUsersUpdate: 'put|/settings/users/:id',
    settingsUsersDelete: 'delete|/settings/users/:id',

    settingsUsersPasswordReset: 'post|/users/password/reset',

    // todo, remove settings prefix
    settingsAccount: 'get|/user/user/account',
    settingsAccountUpdate: 'post|/user/user/account',
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
