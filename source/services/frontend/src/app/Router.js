/**
 * @description Router Entry
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { AuthProvider } from '@/common/hooks/useAuth';
import App from '@/app';
import { HistoryRouter, history } from './history';
import './index.less';

const Router = () => (
  <HistoryRouter history={history}>
    <AuthProvider history={history}>
      <App />
    </AuthProvider>
  </HistoryRouter>
);
export default Router;
