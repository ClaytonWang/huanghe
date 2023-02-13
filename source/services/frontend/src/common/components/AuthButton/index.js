/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-08 18:14:31
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-13 11:52:41
 * @FilePath: /huanghe/source/services/frontend/src/common/components/AuthButton/index.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-11-29 10:48:24
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-21 09:05:48
 * @Description 受权限控制的Button组件, 根据用户权限控制Button是否可点击
 */
import { Button } from 'antd';
import { get, some } from 'lodash';
import { useAuth } from '@/common/hooks/useAuth';

const AuthButton = ({ required, children, condition, ...rest }) => {
  const { user } = useAuth();
  const permissions = get(user, 'permissions', []);
  let props = { ...rest };
  if (required && permissions.indexOf(required) < 0) {
    props = { ...props, disabled: true };
  }
  if (condition && condition.length > 0) {
    if (some(condition, (fn) => !fn(user))) {
      props = { ...props, disabled: true };
    }
  }
  const { type } = props;
  if (type === 'text') {
    return <a {...props}>{children}</a>;
  }
  return <Button {...props}>{children}</Button>;
};
export default AuthButton;
