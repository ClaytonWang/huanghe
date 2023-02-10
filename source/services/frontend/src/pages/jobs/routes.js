/**
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-01-31 16:10:19
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-01-31 16:56:26
 * @FilePath: /frontend/src/pages/jobs/routes.js
 * @Description: Job管理
 */

import { Navigate, Route, Routes } from 'react-router-dom';
import JobList from './list';
import JobUpdate from './update';
import JobDetail from './detail';

const JobRoutes = () => (
  <Routes>
    <Route path="" element={<Navigate to="list" />} />
    <Route path="list" element={<JobList />} />
    <Route path="list/create" element={<JobUpdate />} />
    <Route path="list/update" element={<JobUpdate />} />
    <Route path="list/copy" element={<JobUpdate />} />
    <Route path="list/detail" element={<JobDetail />} />
  </Routes>
);
export default JobRoutes;

export const JobsPages = [JobList, JobUpdate, JobDetail];
