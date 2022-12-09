/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-11-29 10:48:24
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-09 13:49:17
 * @Description 设置页面路由配置
 */
import { Navigate, Route, Routes } from 'react-router-dom';
import UsersList from './users/list';

const SettingsRoutes = () => (
  <Routes>
    <Route path="" element={<Navigate to="users" />} />
    <Route path="users" element={<UsersList />} />
  </Routes>
);
export default SettingsRoutes;
