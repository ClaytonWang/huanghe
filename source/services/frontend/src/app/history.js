/**
 * @description
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import React from 'react';
import { createHashHistory } from 'history';
import { Router } from 'react-router-dom';

export const history = createHashHistory();

export const HistoryRouter = ({ history, children }) => {
  const [state, setState] = React.useState({
    action: history.action,
    location: history.location,
  });

  React.useLayoutEffect(() => {
    history.listen(setState);
  }, [history]);

  return React.createElement(
    Router,
    Object.assign({ children, navigator: history }, state)
  );
};
