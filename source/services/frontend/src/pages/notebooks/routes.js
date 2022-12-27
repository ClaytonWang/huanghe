/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-12-14 19:28:51
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-14 19:29:28
 * @Description Notebook管理
 */
import { Navigate, Route, Routes } from 'react-router-dom';
import NotebooksList from './list';
import NotebookUpdate from './update';

const NotebooksRoutes = () => (
  <Routes>
    <Route path="" element={<Navigate to="list" />} />
    <Route path="list" element={<NotebooksList />} />
    <Route path="list/create" element={<NotebookUpdate />} />
    <Route path="list/update" element={<NotebookUpdate />} />
  </Routes>
);
export default NotebooksRoutes;
