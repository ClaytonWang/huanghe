/**
 * @description Header Nav
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */

import { Layout } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import { useAuth } from '@/common/hooks/useAuth';
import logo from '@/dbr-logo.png';
import './index.less';

const { Header } = Layout;

const HeaderNav = () => {
  const { user } = useAuth();
  return (
    <Header className="dbr-header">
      <div className="dbr-logo">
        <img src={logo} />
      </div>
      <div className="user-info">
        <UserOutlined />
        {user.userName || null}
      </div>
    </Header>
  );
};

export default HeaderNav;
