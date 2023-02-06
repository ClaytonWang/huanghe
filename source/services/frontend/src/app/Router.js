/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-01-31 15:07:28
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-03 17:06:19
 * @FilePath: /huanghe/source/services/frontend/src/app/Router.js
 * @Description: Router Entry
 */
import { AuthProvider } from '@/common/hooks/useAuth';
import { MultiProvider } from '@/common/hooks/MultiProvider';
import { RoutesProvider } from '@/common/hooks/RoutesProvider';
import App from '@/app';
import { HistoryRouter, history } from './history';
import './index.less';

const Router = () => (
  <HistoryRouter history={history}>
    <MultiProvider
      providers={[
        <AuthProvider history={history} key="auth" />,
        <RoutesProvider key="routes" />,
      ]}
    >
      <App />
    </MultiProvider>
  </HistoryRouter>
);
export default Router;
