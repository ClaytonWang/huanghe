/**
 * @description 面包屑导航
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { useLocation, Link } from 'react-router-dom';
import { useCallback, useEffect, useState } from 'react';
import { Breadcrumb } from 'antd';
import { breadcrumbConfig } from '@/common/utils/config';

const BreadcrumbNav = () => {
  const location = useLocation();
  const [routes, setRoutes] = useState([]);

  const genRoutes = useCallback(() => {
    const routes = [];
    const paths = location.pathname.split('/');
    paths.reduce((prev, next) => {
      if (!next) {
        return prev;
      }
      const path = `${prev}/${next}`;
      if (breadcrumbConfig[path]) {
        routes.push({
          path,
          breadcrumbName: breadcrumbConfig[path],
        });
      }
      return path;
    }, '');
    return routes;
  }, [location.pathname]);
  const itemRender = (route, _params, routes, paths) => {
    const last = routes.indexOf(route) === routes.length - 1;
    return last ? (
      <span>{route.breadcrumbName}</span>
    ) : (
      <Link to={`/${paths.join('/')}`}>{route.breadcrumbName}</Link>
    );
  };

  useEffect(() => {
    setRoutes(genRoutes());
  }, [genRoutes]);

  return <Breadcrumb itemRender={itemRender} routes={routes} />;
};
export default BreadcrumbNav;
