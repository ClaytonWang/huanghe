/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-12-07 17:13:41
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-07 18:54:15
 * @Description 存储管理
 */
import { Navigate, Route, Routes } from 'react-router-dom';
import StoragesList from './list';

const StorageRoutes = () => (
  <Routes>
    <Route path="" element={<Navigate to="list" />} />
    <Route path="list" element={<StoragesList />} />
  </Routes>
);
export default StorageRoutes;
