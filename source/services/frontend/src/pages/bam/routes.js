/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-11-29 10:48:24
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-02 14:18:18
 * @Description 后台管理模块路由配置
 */
import { Navigate, Route, Routes } from 'react-router-dom';
import ProjectsList from './projects/list';
import UserList from './users/list';

const BamRoutes = () => (
  <Routes>
    <Route path="" element={<Navigate to="bam" />} />
    <Route path="projects" element={<ProjectsList />} />
    <Route path="users" element={<UserList />} />
  </Routes>
);
export default BamRoutes;
