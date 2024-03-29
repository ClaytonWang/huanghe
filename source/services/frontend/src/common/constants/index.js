/**
 * @Author: liguanlin<guanlin.li@digitalbrain.cn> junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-01-31 15:07:28
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 *               guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-02-28 20:35:31
 * @FilePath: /frontend/src/common/constants/index.js
 * @Description: Global Constants
 */
// 用户角色
export const USER_ROLE = {
  admin: '超级管理员',
  owner: '项目负责人',
  user: '普通用户',
};
export const ADMIN = 'admin';
export const OWNER = 'owner';
export const USER = 'user';
// 普通用户权限
export const ACCESS_MAP = {
  edit: '编辑',
  readonly: '查看',
};
// 计划名词
export const PLANS_MAP = {
  name: '计划名称',
  creator: '创建人',
  createTime: '创建时间',
  lastEditTime: '最后编辑时间',
  organization: '组织',
  status: '状态',
  saveCost: '预计节省',
  users: '普通用户',
};
// 正则
export const EMAIL_REG = /^[\w._]+@[\w-]+(\.[\w]+)*(\.[\w]{2,6})$/;
// 默认密码
export const DEFAULT_PASSWORD = 'syy12345';
// Modal Type
export const INFO = 'info';
export const PASSWORD = 'password';
export const CREATE = 'create';
export const EDIT = 'edit';
export const UPDATE = 'update';
export const COPY = 'copy';
export const DEBUG = '调试';

// notebooks
export const NOTEBOOK_STATUS = {
  starting: '01',
  stopping: '02',
  pending: '03',
  running: '04',
  stopped: '05',
  error: '06',
};
export const START = 'start';
export const STOP = 'stop';
export const NOTEBOOK_ACTION = {
  [START]: 1,
  [STOP]: 0,
};

export const JOB_ACTION = {
  [START]: 1,
  [STOP]: 0,
};
export const ACTION = {
  [START]: 1,
  [STOP]: 0,
};
export const ADDRESS_TYPE = {
  private: '私网',
  public: '公网',
};
