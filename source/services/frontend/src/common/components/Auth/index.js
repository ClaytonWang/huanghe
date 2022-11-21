/**
 * @description 权限校验组件，有权限显示，无权限隐藏
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { get } from 'lodash';
import { useAuth } from '@/common/hooks/useAuth';
const Auth = ({ required, children }) => {
  const { user } = useAuth();
  const permissions = get(user, 'permissions', []);
  return permissions.indexOf(required) > -1 ? children : null;
};
export default Auth;
