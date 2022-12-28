/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2022-12-27 16:01:51
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2022-12-27 16:06:48
 * @FilePath: /frontend/src/pages/overview/index.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
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
