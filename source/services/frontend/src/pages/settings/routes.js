/**
 * @description
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { Navigate, Route, Routes } from 'react-router-dom';
import Account from './account';
import UsersList from './users/list';

const SettingsRoutes = () => (
  <Routes>
    <Route path="" element={<Navigate to="account" />} />
    <Route path="account" element={<Account />} />
    <Route path="users" element={<UsersList />} />
  </Routes>
);
export default SettingsRoutes;
