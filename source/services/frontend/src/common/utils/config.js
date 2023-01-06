/**
 * @description 全局属性
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
const APIV1 = '/api/v1';
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
    login: 'post|/user/auth/login',
    logout: 'put|/user/auth/logout',

    // bam
    bamProjectsList: 'get|/user/project',
    bamProjectsCreate: 'post|/user/project',
    bamProjectsUpdate: 'put|/user/project/:project_id',
    bamProjectsDelete: 'delete|/user/project/:project_id',
    // bamUsersList: 'get|/user/bam/users',
    bamUsersList: 'get|/user/user',
    bamUsersCreate: 'post|/user/user',
    bamUsersUpdate: 'put|/user/user/:user_id',
    bamUsersDelete: 'delete|/user/user/:user_id',
    userListItems: 'get|/user/user/items',

    // settings
    settingsUsersList: 'get|/user/settings/user',
    settingsUsersCreate: 'post|/user/settings/user',
    settingsUsersUpdate: 'put|/user/settings/user/:pk',
    settingsUsersDelete: 'delete|/user/settings/user/:pk',

    // todo, remove settings prefix
    settingsAccount: 'get|/user/user/account',
    settingsAccountUpdate: 'post|/user/user/account',

    // FIXME: 后端获取指定菜单的权限接口
    access: 'get|/user/pms/menu',
    storagesList: 'get|/storages/volume',
    storagesListCreate: 'post|/storages/volume',
    storagesListUpdate: 'put|/storages/volume/:id',
    storagesListDelete: 'delete|/storages/volume/:id',
    storagesListReset: 'post|/storages/volume/:id/reset',

    notebooksList: 'get|/notebook/notebooks',
    notebooksDetail: 'get|/notebook/notebooks/:id',
    notebooksListCreate: 'post|/notebook/notebooks',
    notebooksListAction: 'post|/notebook/notebooks/:id',
    notebooksListUpdate: 'put|/notebook/notebooks/:id',
    notebooksListDelete: 'delete|/notebook/notebooks/:id',
    imagesList: 'get|/notebook/image',
    sourceList: 'get|/notebook/source',
  },
  breadcrumbConfig: {
    '/overview/list': '总览',
    '/bam/projects': '项目管理',
    '/bam/users': '用户管理',
    '/settings/users': '用户列表',

    '/settings/account': '我的账号',

    '/storages/list': '存储管理',

    '/notebooks/list': 'Notebook列表',
    '/notebooks/list/update': '编辑Notebook',
    '/notebooks/list/create': '创建Notebook',
  },
  menuItemsConfig: [
    {
      key: 'overview',
      label: '总览',
      icon: 'overview',
      children: [
        {
          key: 'overview.list',
          label: '总览',
        },
      ],
    },
    {
      key: 'bam',
      label: '后台管理',
      icon: 'bam',
      permission: 'bam',
      children: [
        {
          key: 'bam.projects',
          label: '项目管理',
          permission: 'bam.projects',
        },
        {
          key: 'bam.users',
          label: '用户管理',
          permission: 'bam.users',
        },
      ],
    },
    {
      key: 'notebooks',
      label: 'Notebook管理',
      icon: 'notebooks',
      permission: 'notebooks',
      children: [
        {
          key: 'notebooks.list',
          label: 'Notebook列表',
          permission: 'notebooks.list',
        },
      ],
    },
    {
      key: 'storages',
      label: '存储',
      icon: 'storages',
      permission: 'storages',
      children: [
        {
          key: 'storages.list',
          label: '存储管理',
          permission: 'storages.list',
        },
      ],
    },
    {
      key: 'settings',
      label: '设置',
      icon: 'settings',
      permission: 'settings',
      children: [
        {
          key: 'settings.users',
          label: '用户权限',
          permission: 'settings.users',
        },
      ],
    },
  ],
};
