/**
 * @description 我的账号页
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { Card, Row, Col, Modal, Form, Input, Button, message } from 'antd';
import { useEffect, useState } from 'react';
import { ExclamationCircleOutlined } from '@ant-design/icons';
import { useAuth } from '@/common/hooks/useAuth';
import api from '@/common/api';
import { ROLE_MAP, PASSWORD, INFO } from '@/common/constants';
import { FormModal } from '@/common/components';
import './index.less';

const Account = () => {
  const [showInfoModal, setShowInfoModal] = useState(false);
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [infoValues, setInfoValues] = useState(null);
  const { user, logout, loadAccount } = useAuth();

  useEffect(() => {}, []);

  const basicItems = [
    {
      title: '姓名',
      name: 'userName',
    },
    {
      title: '角色',
      name: 'role',
      render(value) {
        if (!value) return '-';
        return ROLE_MAP[value] || value;
      },
    },
    {
      title: '组织',
      name: 'organization',
      render(value) {
        return (value && value.name) || '-';
      },
    },
    {
      title: '邮箱',
      name: 'email',
    },
  ];

  const openModal = (type) => {
    if (type === INFO) {
      setInfoValues({ userName: user.userName });
      setShowInfoModal(true);
    } else if (type === PASSWORD) {
      setShowPasswordModal(true);
    }
  };
  const closeModal = () => {
    setShowInfoModal(false);
    setShowPasswordModal(false);
  };
  const handleLogoutClicked = () => {
    Modal.confirm({
      title: '确定要退出账号吗？',
      icon: <ExclamationCircleOutlined />,
      okText: '确认',
      cancelText: '取消',
      onOk: async () => {
        logout();
      },
    });
  };
  const handleEditClicked = (type) => {
    openModal(type);
  };
  const handleEditCancel = () => {
    closeModal();
  };
  const handleInfoSubmit = async (values) => {
    try {
      await api.settingsAccountUpdate({ ...values });
      message.success('用户名修改成功！');
      closeModal();
      loadAccount();
    } catch (error) {
      console.log(error);
    }
  };
  const handlePasswordSubmit = async (values) => {
    try {
      const { originPassword, password } = values;
      await api.settingsAccountUpdate({
        originPassword,
        password,
      });
      message.success('密码修改成功！');
      closeModal();
      logout();
    } catch (error) {
      console.log(error);
    }
  };
  const renderContent = (data) => {
    const items = basicItems.map((item, index) => {
      const { title, name, render } = item;
      const value = data[name];
      return (
        <Row key={index} gutter={{ xs: 8, sm: 16, md: 24, lg: 32 }}>
          <Col className="gutter-row account-info-col" span={6}>
            <span className="account-info-label">{title}: </span>
            <span>{render ? render(value) : value}</span>
          </Col>
        </Row>
      );
    });
    return [...items];
  };
  return (
    <div className="account-detail dbr-content-container">
      <div className="batch-command">
        <Button
          required="plans.update.edit"
          onClick={handleLogoutClicked}
          className="alert"
        >
          退出账号
        </Button>
      </div>
      <Card
        title="基本信息"
        bordered={false}
        className="account-detail-info dbr-content-item"
        extra={
          <>
            <Button onClick={() => handleEditClicked(INFO)}>修改姓名</Button>
            <Button onClick={() => handleEditClicked(PASSWORD)}>
              修改密码
            </Button>
          </>
        }
      >
        <div className="account-detail-info-content">
          {renderContent({
            userName: user.userName,
            organization: user.organization,
            role: user.role,
            email: user.email,
          })}
        </div>
      </Card>
      {showInfoModal && (
        <FormModal
          title="编辑个人信息"
          okText="保存"
          initialValues={infoValues}
          onSubmit={handleInfoSubmit}
          onCancel={handleEditCancel}
        >
          <Form.Item
            name="userName"
            label="姓名"
            rules={[{ required: true, message: '请输用户名' }]}
          >
            <Input placeholder="请输入您的姓名" />
          </Form.Item>
        </FormModal>
      )}
      {showPasswordModal && (
        <FormModal
          title="修改密码"
          onSubmit={handlePasswordSubmit}
          onCancel={handleEditCancel}
        >
          <Form.Item
            name="originPassword"
            label="当前密码"
            rules={[{ required: true, message: '请输入原始密码' }]}
          >
            <Input.Password placeholder="请输入当前密码" />
          </Form.Item>
          <Form.Item
            name="password"
            label="新密码"
            hasFeedback
            rules={[
              { required: true, message: '请输入新密码' },
              { len: 8, message: '请输入八位密码' },
            ]}
          >
            <Input.Password placeholder="请输入新密码" />
          </Form.Item>
          <Form.Item
            name="confirm"
            label="再次输入新密码"
            dependencies={['password']}
            hasFeedback
            rules={[
              { required: true, message: '请再次输入新密码' },
              { len: 8, message: '请输入八位密码' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('两次输入密码不一致！'));
                },
              }),
            ]}
          >
            <Input.Password placeholder="请再次输入新密码" />
          </Form.Item>
        </FormModal>
      )}
    </div>
  );
};
export default Account;
