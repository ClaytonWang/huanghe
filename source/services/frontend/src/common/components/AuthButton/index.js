/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-11-29 10:48:24
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-21 09:05:48
 * @Description 受权限控制的Button组件, 根据用户权限控制Button是否可点击
 */
import { Button } from 'antd';
import { get } from 'lodash';
import { useAuth } from '@/common/hooks/useAuth';

const AuthButton = ({ required, children, condition, ...rest }) => {
  const { user } = useAuth();
  const permissions = get(user, 'permissions', []);
  let props = { ...rest };
  if (permissions.indexOf(required) < 0) {
    props = { ...props, disabled: true };
  }
  if (condition && !condition()) {
    props = { ...props, disabled: true };
  }
  return <Button {...props}>{children}</Button>;
};
export default AuthButton;
