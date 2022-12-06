/**
 * @description 全局属性
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
const APIV1 = '/api/v1/user';
// const DEV = '';
module.exports = {
  name: '决策智能开发平台',
  footerText: 'Shanghai Digital Brain.Lmt.',
  logo: 'static/logo.svg',
  CORS: [],
  apiPrefix: APIV1,
  apiUriParamsPattern: /:([_a-zA-Z0-9]+)/g,
  api: {
    // login
    login: 'post|/auth/login',
    logout: 'put|/auth/logout',

    // bam
    bamProjectsList: 'get|/project',
    bamProjectsCreate: 'post|/project',
    bamProjectsUpdate: 'put|/project/:project_id',
    bamProjectsDelete: 'delete|/project/:project_id',
    // bamUsersList: 'get|/bam/users',
    bamUsersList: 'get|/user',
    bamUsersCreate: 'post|/user',
    bamUsersUpdate: 'put|/user/:user_id',
    bamUsersDelete: 'delete|/user/:user_id',

    // settings
    settingsUsersList: 'get|/settings/user',
    settingsUsersCreate: 'post|/settings/user',
    settingsUsersUpdate: 'post|/settings/user',
    settingsUsersDelete: 'post|/settings/user',

    // todo, remove settings prefix
    settingsAccount: 'get|/user/account',
    settingsAccountUpdate: 'post|/user/account',

    // FIXME: 后端获取指定菜单的权限接口
    access: 'get|/pms/menu',
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
