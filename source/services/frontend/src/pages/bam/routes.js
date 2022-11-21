/**
 * @description
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { Navigate, Route, Routes } from 'react-router-dom';
import ProjectList from './projects/list';
import UserList from './users/list';

const BamRoutes = () => (
  <Routes>
    <Route path="" element={<Navigate to="bam" />} />
    <Route path="projects" element={<ProjectList />} />
    <Route path="users" element={<UserList />} />
  </Routes>
);
export default BamRoutes;
