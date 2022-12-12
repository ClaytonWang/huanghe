/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-11-29 10:48:24
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-08 11:05:28
 * @Description 功能页路由配置
 */
import { Route, Routes } from 'react-router-dom';
import ProtectedLayout from '@/common/components/ProtectedLayout';
import Bam from '@/pages/bam';
import Settings from '@/pages/settings';
import Storages from '@/pages/storages';
import './index.less';

const Pages = () => (
  <Routes>
    <Route path="/*" element={<ProtectedLayout />}>
      <Route path="bam/*" element={<Bam />} />
      <Route path="settings/*" element={<Settings />} />
      <Route path="storages/*" element={<Storages />} />
    </Route>
  </Routes>
);

export default Pages;
