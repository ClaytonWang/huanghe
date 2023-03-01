/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2023-02-28 18:03:39
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-02-28 20:50:25
 * @FilePath: /frontend/src/pages/routes.js
 * @Description: 功能页路由配置
 */
import { Route, Routes } from 'react-router-dom';
import ProtectedLayout from '@/common/components/ProtectedLayout';
import Bam from '@/pages/bam';
import Settings from '@/pages/settings';
import Storages from '@/pages/storages';
import Notebooks from '@/pages/notebooks';
import Jobs from '@/pages/jobs';
import Overview from '@/pages/overview';
import Services from '@/pages/services';
import './index.less';

const PagesRoutes = () => (
  <Routes>
    <Route path="/*" element={<ProtectedLayout />}>
      <Route path="overview/*" element={<Overview />} />
      <Route path="bam/*" element={<Bam />} />
      <Route path="settings/*" element={<Settings />} />
      <Route path="storages/*" element={<Storages />} />
      <Route path="notebooks/*" element={<Notebooks />} />
      <Route path="jobs/*" element={<Jobs />} />
      <Route path="services/*" element={<Services />} />
    </Route>
  </Routes>
);

export default PagesRoutes;
