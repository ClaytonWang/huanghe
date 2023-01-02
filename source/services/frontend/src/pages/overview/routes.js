/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-12-27 16:04:56
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-27 16:06:08
 * @Description 总览
 */
import { Navigate, Route, Routes } from 'react-router-dom';
import OverviewList from './list';

const OverviewRoutes = () => (
  <Routes>
    <Route path="" element={<Navigate to="list" />} />
    <Route path="list" element={<OverviewList />} />
  </Routes>
);
export default OverviewRoutes;
