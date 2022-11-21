/**
 * @description 设置模块
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { Layout } from 'antd';
import BreadcrumbNav from '@/common/components/BreadcrumbNav';
import Routes from './routes';
import './index.less';

const Settings = () => (
  <Layout className="dbr-main-layout">
    <BreadcrumbNav />
    <Routes />
  </Layout>
);
export default Settings;
