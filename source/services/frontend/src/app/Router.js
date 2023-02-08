/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-01-31 15:07:28
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-06 19:51:08
 * @FilePath: /huanghe/source/services/frontend/src/app/Router.js
 * @Description: Router Entry
 */
import { AuthProvider } from '@/common/hooks/useAuth';
import { MultiProvider } from '@/common/hooks/MultiProvider';
import { RoutesProvider } from '@/common/hooks/RoutesProvider';
import { ConfigProvider } from 'antd';
import App from '@/app';
import { HistoryRouter, history } from './history';
import locale from 'antd/es/locale/zh_CN';
import './index.less';

const Router = () => (
  <HistoryRouter history={history}>
    <MultiProvider
      providers={[
        <ConfigProvider locale={locale} key="config" />,
        <AuthProvider history={history} key="auth" />,
        <RoutesProvider key="routes" />,
      ]}
    >
      <App />
    </MultiProvider>
  </HistoryRouter>
);
export default Router;
