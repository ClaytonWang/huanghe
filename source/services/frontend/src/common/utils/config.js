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
    settingsUsersUpdate: 'post|/user/settings/user',
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

    notebooksList: 'get|/notebooks',
    notebooksDetail: 'get|/notebooks/:id',
    notebooksListCreate: 'post|/notebooks',
    notebooksListAction: 'post|/notebooks/:id',
    notebooksListUpdate: 'put|/notebooks/:id',
    notebooksListDelete: 'delete|/notebooks/:id',
    imagesList: 'get|/images',
    sourceList: 'get|/source',
  },
  breadcrumbConfig: {
    '/bam/projects': '项目管理',
    '/bam/users': '用户管理',
    '/settings/users': '用户列表',

    '/settings/account': '我的账号',

    '/storages/list': '存储管理',

    '/notebooks/list': 'Notebook管理',
    '/notebooks/list/update': '编辑Notebook',
    '/notebooks/list/create': '创建Notebook',
  },
  menuItemsConfig: [
    {
      key: 'bam',
      label: '后台管理',
      icon: 'bam',
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
      icon: 'settings',
      children: [
        {
          key: 'settings.users',
          label: '用户权限',
        },
      ],
    },
    {
      key: 'notebooks',
      label: 'Notebook',
      icon: 'notebooks',
      children: [
        {
          key: 'notebooks.list',
          label: 'Notebook管理',
        },
      ],
    },
    {
      key: 'storages',
      label: '存储',
      icon: 'storages',
      children: [
        {
          key: 'storages.list',
          label: '存储管理',
        },
      ],
    },
  ],
};
