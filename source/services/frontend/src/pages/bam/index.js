/**
 * @description 计划中心
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { Layout } from 'antd';
import BreadcrumbNav from '@/common/components/BreadcrumbNav';
import Routes from './routes';

const Bam = () => (
  <Layout className="dbr-main-layout">
    <BreadcrumbNav />
    <Routes />
  </Layout>
);
export default Bam;
