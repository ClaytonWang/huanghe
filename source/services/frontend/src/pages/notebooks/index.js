/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-12-14 16:11:21
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-14 19:30:47
 * @Description Notebook模块
 */
import { Layout } from 'antd';
import BreadcrumbNav from '@/common/components/BreadcrumbNav';
import Routes from './routes';
import './index.less';

const Notebooks = () => (
  <Layout className="dbr-main-layout">
    <BreadcrumbNav />
    <Routes />
  </Layout>
);
export default Notebooks;
