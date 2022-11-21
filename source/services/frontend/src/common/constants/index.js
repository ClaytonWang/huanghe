/**
 * @description Global Constants
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
// 用户角色
export const USER_ROLE = {
  admin: '超级管理员',
  owner: '项目负责人',
  user: '普通用户',
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
// 角色
export const ROLE_MAP = {
  owner: '项目负责人',
  admin: '管理员',
  user: '普通用户',
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
