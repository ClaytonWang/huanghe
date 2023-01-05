/**
 * @description Header Nav
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { useState } from 'react';
import {
  Layout,
  Dropdown,
  Space,
  Menu,
  Modal,
  Select,
  Input,
  Form,
  message,
} from 'antd';
import Icon, {
  DownOutlined,
  ExclamationCircleOutlined,
} from '@ant-design/icons';
import { useAuth } from '@/common/hooks/useAuth';
import logo from '@/dbr-logo.png';
import api from '@/common/api';
import FormModal from '@/common/components/FormModal';
import { parseKVToKeyValue } from '@/common/utils/helper';
import { USER_ROLE } from '@/common/constants';
import Icons from '../Icon';
import './index.less';

const { Header } = Layout;
const { Option } = Select;

const HeaderNav = () => {
  const { user, logout } = useAuth();
  const [showAccountModal, setShowAccountModal] = useState(false);

  const handleAccountClicked = () => {
    setShowAccountModal(true);
  };
  const handleLogoutClicked = () => {
    Modal.confirm({
      title: '确定要退出登陆吗？',
      icon: <ExclamationCircleOutlined />,
      okText: '确认',
      cancelText: '取消',
      onOk: async () => {
        try {
          await api.logout();
          logout();
        } catch (error) {
          console.log(error);
        }
      },
    });
  };
  const handleDropdownClicked = ({ key }) => {
    const methods = {
      account: () => handleAccountClicked(),
      logout: () => handleLogoutClicked(),
    };
    return methods[key]();
  };
  const closeAccountModal = () => {
    setShowAccountModal(false);
  };
  const updateAccount = async (values) => {
    try {
      await api.settingsAccountUpdate(values);
      message.success('个人信息修改成功！即将跳转至首页重新登陆...');
      closeAccountModal();
      // 个人信息修改成功后，重新登陆。
      setTimeout(() => {
        logout();
      }, 1000);
    } catch (error) {
      console.log(error);
      closeAccountModal();
    }
  };
  const handleAccountSubmit = (values) => {
    updateAccount({
      ...values,
    });
  };
  const handleAccountCancel = () => {
    closeAccountModal();
  };
  const menu = (
    <Menu onClick={handleDropdownClicked}>
      <Menu.Item key="account">个人信息</Menu.Item>
      <Menu.Item key="logout">退出登陆</Menu.Item>
    </Menu>
  );
  return (
    <>
      <Header className="dbr-header">
        <div className="dbr-title">
          <img src={logo} />
          <span>决策中台</span>
        </div>
        <div className="user-info">
          <Icon component={Icons.account} />
          <Dropdown overlay={menu}>
            <a onClick={(e) => e.preventDefault()}>
              <Space>
                {user.username || null}
                <DownOutlined />
              </Space>
            </a>
          </Dropdown>
        </div>
      </Header>
      {showAccountModal && (
        <FormModal
          title="个人信息"
          okText="保存"
          cancelText="取消"
          initialValues={user}
          onSubmit={handleAccountSubmit}
          onCancel={handleAccountCancel}
        >
          <Form.Item
            label="姓名"
            name="username"
            rules={[{ required: true, message: '请输入用户名' }]}
          >
            <Input placeholder="请输入姓名" disabled />
          </Form.Item>
          <Form.Item label="角色" name="role">
            <Select disabled>
              <Option key="all" value="all">
                全部
              </Option>
              {parseKVToKeyValue(USER_ROLE, 'k', 'v').map(({ k, v }) => (
                <Option key={k} value={k}>
                  {v}
                </Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item label="旧密码" name="oldPassword">
            <Input.Password placeholder="请输入旧密码" />
          </Form.Item>
          <Form.Item
            label="新密码"
            name="password"
            rules={[{ len: 8, message: '请输入8位数密码' }]}
          >
            <Input.Password placeholder="请输入新密码" />
          </Form.Item>
        </FormModal>
      )}
    </>
  );
};

export default HeaderNav;
