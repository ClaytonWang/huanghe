/**
 * @description App Entry
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { createRoot } from 'react-dom/client';
import Router from '@/app/Router';
import moment from 'moment';
import 'moment/locale/zh-cn';
import './common/api';
import './common/css/index.less';

moment.locale('zh-cn');
window.moment = moment;
const container = document.getElementById('root');
const root = createRoot(container);
root.render(<Router />);
