/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-11-29 10:48:24
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2023-01-08 09:59:56
 * @Description App
 */
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '@/common/hooks/useAuth';
import { SystemProvider } from '@/common/hooks/useSystem';
import Login from '@/pages/login';
import Pages from '@/pages';

const App = () => {
  const { token } = useAuth();
  const renderLogin = () => (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/*" element={<Navigate to="login" />} />
    </Routes>
  );
  const renderApp = () => (
    <SystemProvider>
      <Pages />
    </SystemProvider>
  );
  return !token ? renderLogin() : renderApp();
};
export default App;
