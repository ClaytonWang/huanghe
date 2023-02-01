/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2022-12-27 16:01:51
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-01 16:01:33
 * @FilePath: /frontend/src/pages/overview/index.js
 * @Description:
 */

import { Layout } from 'antd';
import BreadcrumbNav from '@/common/components/BreadcrumbNav';
import Routes from './routes';
import './index.less';

const Overview = () => (
  <Layout className="dbr-main-layout">
    <BreadcrumbNav />
    <Routes />
  </Layout>
);
export default Overview;
