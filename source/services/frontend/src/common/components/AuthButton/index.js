/**
 * @description 受权限控制的Button组件, 根据用户权限控制Button是否可点击
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { Button } from 'antd';
import { get } from 'lodash';
import { useAuth } from '@/common/hooks/useAuth';

const AuthButton = ({ required, children, ...rest }) => {
  const { user } = useAuth();
  const permissions = get(user, 'permissions', []);
  let props = { ...rest };
  if (permissions.indexOf(required) < 0) {
    props = { ...props, disabled: true };
  }
  return <Button {...props}>{children}</Button>;
};
export default AuthButton;
