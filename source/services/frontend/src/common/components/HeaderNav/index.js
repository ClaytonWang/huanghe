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
import {
  UserOutlined,
  DownOutlined,
  ExclamationCircleOutlined,
} from '@ant-design/icons';
import { useAuth } from '@/common/hooks/useAuth';
import logo from '@/dbr-logo.png';
import api from '@/common/api';
import FormModal from '@/common/components/FormModal';
import './index.less';
import { parseKVToKeyValue } from '@/common/utils/helper';
import { USER_ROLE } from '@/common/constants';
import { b64 } from '@/common/utils/util';

const { Header } = Layout;
const { Option } = Select;

const HeaderNav = () => {
  const { user, logout, loadAccount } = useAuth();
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
      message.success('个人信息修改成功！');
      closeAccountModal();
      // reload account
      loadAccount();
    } catch (error) {
      console.log(error);
      closeAccountModal();
    }
  };
  const handleAccountSubmit = (values) => {
    updateAccount({
      ...values,
      oldPassword: b64.encode(values.oldPassword),
      password: b64.encode(values.password),
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
        <div className="dbr-logo">
          <img src={logo} />
        </div>
        <div className="user-info">
          <UserOutlined />
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
            rules={[{ required: true, message: '请输入用户姓名' }]}
          >
            <Input placeholder="请输入姓名" />
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
          <Form.Item
            label="旧密码"
            name="oldPassword"
            rules={[{ required: true, message: '请输入旧密码' }]}
          >
            <Input.Password placeholder="请输入旧密码" />
          </Form.Item>
          <Form.Item
            label="新密码"
            name="password"
            rules={[
              { required: true, message: '请输入新密码' },
              { len: 8, message: '请输入8位数密码' },
            ]}
          >
            <Input.Password placeholder="请输入新密码" />
          </Form.Item>
        </FormModal>
      )}
    </>
  );
};

export default HeaderNav;
