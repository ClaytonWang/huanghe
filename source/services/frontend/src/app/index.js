/**
 * @description App
 * @author liguanlin<guanlin.li@digitalbrain.cn>
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
