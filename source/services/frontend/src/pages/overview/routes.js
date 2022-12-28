/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2022-12-27 16:04:56
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2022-12-27 16:06:08
 * @FilePath: /frontend/src/pages/overview/routes.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
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
