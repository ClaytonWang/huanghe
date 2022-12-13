/**
 * @description 登陆页
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { Form, Input, Button } from 'antd';
import Icon, { LockOutlined, UserOutlined } from '@ant-design/icons';
import { useAuth } from '@/common/hooks/useAuth';
import { name } from '@/common/utils/config';
import Icons from '@/common/components/Icon';
import bg from '@/common/images/carousel_0.png';
import './index.less';

const LoginForm = () => {
  const { login } = useAuth();
  const onFinish = (values) => {
    login({
      ...values,
    });
  };
  return (
    <>
      <Form
        title="登录"
        name="normal_login"
        className="login-form"
        onFinish={onFinish}
        layout="vertical"
      >
        <Form.Item
          name="email"
          rules={[
            {
              required: true,
              message: '请输入注册邮箱!',
            },
            {
              pattern: /^[\w.]+@[\w]+(\.[\w]+)+$/,
              message: '请输入有效邮箱！',
            },
          ]}
        >
          <Input
            prefix={<UserOutlined className="site-form-item-icon" />}
            placeholder="邮箱"
          />
        </Form.Item>
        <Form.Item
          name="password"
          rules={[
            {
              required: true,
              message: '请输入登录密码!',
            },
          ]}
        >
          <Input
            prefix={<LockOutlined className="site-form-item-icon" />}
            type="password"
            placeholder="密码"
          />
        </Form.Item>
        <Form.Item>
          <Button
            type="primary"
            htmlType="submit"
            className="login-form-button"
          >
            登陆
          </Button>
        </Form.Item>
      </Form>
    </>
  );
};
const Login = () => (
  <div className="login">
    <img className="bg-image" src={bg} />
    <div className="title">
      <Icon
        component={Icons.develop}
        style={{ fontSize: '20em', margin: 'auto -10px auto 10%' }}
      />
      <span>{name}</span>
    </div>
    <LoginForm />
  </div>
);
export default Login;
