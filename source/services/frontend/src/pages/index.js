/**
 * @description 功能页路由配置
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { Route, Routes } from 'react-router-dom';
import ProtectedLayout from '@/common/components/ProtectedLayout';
import Bam from '@/pages/bam';
import Settings from '@/pages/settings';
import './index.less';

const Pages = () => (
  <Routes>
    <Route path="/*" element={<ProtectedLayout />}>
      <Route path="bam/*" element={<Bam />} />
      <Route path="settings/*" element={<Settings />} />
    </Route>
  </Routes>
);

export default Pages;
