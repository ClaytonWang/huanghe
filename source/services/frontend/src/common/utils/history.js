/**
 * @description History Utils
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */

import { createBrowserHistory } from 'history';

const history = createBrowserHistory();

export const { push, replace, go, goBack, goForward } = history;
export default history;
