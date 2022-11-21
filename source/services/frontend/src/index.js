/**
 * @description App Entry
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { createRoot } from 'react-dom/client';
import Router from '@/app/Router';
import './common/api';
import './common/css/index.less';

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<Router />);
