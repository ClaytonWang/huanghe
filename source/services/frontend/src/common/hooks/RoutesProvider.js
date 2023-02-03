/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-03 16:00:40
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-03 19:31:07
 * @FilePath: /huanghe/source/services/frontend/src/providers/RoutesProvider.js
 * @Description: RoutesProvider
 */
import { createContext, useContext, useMemo, useState, useEffect } from 'react';
import { matchPath, useLocation } from 'react-router';
import { pageSetToRoutes } from '@/common/utils/helper';
import { NotebooksPages } from '@/pages/notebooks/routes';

export const RoutesContext = createContext();

const findMacthingComponents = (path, routesMap, parentPath = '') => {
  const result = [];

  const match = routesMap.find((route) => {
    const matchingPath = `${parentPath}${route.path}`;
    const match = matchPath({ path: matchingPath }, path);

    return match;
  });

  if (match) {
    const routePath = `${parentPath}${match.path}`;

    result.push({ ...match, path: routePath });

    if (match.routes) {
      result.push(...findMacthingComponents(path, match.routes, routePath));
    }
  }

  return result;
};

export const useFixedLocation = () => {
  const location = useLocation();

  const result = useMemo(() => location.location ?? location, [location]);

  return result;
};

export const useContextComponent = () => {
  const ctx = useContext(RoutesContext);
  const { component: ContextComponent, props: contextProps } =
    ctx?.currentContext ?? {};

  return { ContextComponent, contextProps };
};

export const RoutesProvider = ({ children }) => {
  const location = useFixedLocation();
  const [currentContext, setCurrentContext] = useState(null);
  const [currentContextProps, setCurrentContextProps] = useState(null);

  const routesMap = useMemo(() => {
    const pages = [...NotebooksPages];
    return pageSetToRoutes(pages);
  }, []);

  const routesChain = useMemo(
    () => findMacthingComponents(location.pathname, routesMap),
    [routesMap, location]
  );

  const lastRoute = useMemo(
    () => routesChain.filter((r) => !r.modal).slice(-1)[0],
    [routesChain]
  );

  const contextValue = useMemo(
    () => ({
      currentContext,
      setContextProps: setCurrentContextProps,
    }),
    [currentContext, setCurrentContextProps]
  );

  useEffect(() => {
    const ContextComponent = lastRoute?.context;

    setCurrentContext({
      component: ContextComponent ?? null,
      props: currentContextProps,
    });
  }, [lastRoute, currentContextProps]);

  return (
    <RoutesContext.Provider value={contextValue}>
      {children}
    </RoutesContext.Provider>
  );
};

export const useContextProps = () => {
  const setProps = useContext(RoutesContext).setContextProps;

  return useMemo(() => setProps, [setProps]);
};
