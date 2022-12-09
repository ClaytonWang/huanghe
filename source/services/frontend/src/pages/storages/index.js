/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-12-07 17:11:43
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-07 18:59:08
 * @Description 存储模块
 */
import { Layout } from 'antd';
import BreadcrumbNav from '@/common/components/BreadcrumbNav';
import Routes from './routes';
import './index.less';

const Storages = () => (
  <Layout className="dbr-main-layout">
    <BreadcrumbNav />
    <Routes />
  </Layout>
);
export default Storages;
