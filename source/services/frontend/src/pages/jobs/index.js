/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-01-31 16:10:19
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-01-31 16:58:02
 * @FilePath: /frontend/src/pages/jobs/index.js
 * @Description: Job模块
 */
import { Layout } from 'antd';
import BreadcrumbNav from '@/common/components/BreadcrumbNav';
import Routes from './routes';
import './index.less';

const Jobs = () => (
  <Layout className="dbr-main-layout">
    <BreadcrumbNav />
    <Routes />
  </Layout>
);
export default Jobs;
