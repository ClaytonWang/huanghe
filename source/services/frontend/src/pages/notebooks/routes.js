/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-01-31 15:07:28
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-03 17:51:30
 * @FilePath: /huanghe/source/services/frontend/src/pages/notebooks/routes.js
 * @Description: Router page
 */
import { Navigate, Route, Routes } from 'react-router-dom';
import NotebooksList from './list';
import NotebookUpdate from './update';
import NotebookDetail from './detail';

const NotebooksRoutes = () => (
  <Routes>
    <Route path="" element={<Navigate to="list" />} />
    <Route path="list" element={<NotebooksList />} />
    <Route path="list/create" element={<NotebookUpdate />} />
    <Route path="list/update" element={<NotebookUpdate />} />
    <Route path="list/detail" element={<NotebookDetail />} />
  </Routes>
);
export default NotebooksRoutes;

export const NotebooksPages = [NotebooksList, NotebookUpdate, NotebookDetail];
