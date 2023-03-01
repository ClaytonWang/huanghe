/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2023-02-28 15:30:19
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-02-28 20:16:41
 * @FilePath: /frontend/src/pages/services/routes.js
 * @Description: 服务部署模块路由
 */
import { Navigate, Route, Routes } from 'react-router-dom';
import ServicesList from './list';
import ServicesUpdate from './update';
import ServicesDetail from './detail';

const ServicesRoutes = () => (
  <Routes>
    <Route path="" element={<Navigate to="list" />} />
    <Route path="list" element={<ServicesList />} />
    <Route path="list/create" element={<ServicesUpdate />} />
    <Route path="list/update" element={<ServicesUpdate />} />
    <Route path="list/detail" element={<ServicesDetail />} />
  </Routes>
);
export default ServicesRoutes;

export const ServicesPages = [ServicesList, ServicesUpdate, ServicesDetail];
