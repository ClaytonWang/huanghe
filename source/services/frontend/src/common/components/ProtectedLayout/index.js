/**
 * @description Authenticate user info before render component
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { Link, Outlet, useLocation } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import { get, find } from 'lodash';
import { useCallback, useMemo } from 'react';
import HeaderNav from '@/common/components/HeaderNav';
import { useAuth } from '@/common/hooks/useAuth';
import { tranverseTree, isLeafNode } from '@/common/utils/helper';
import { menuItemsConfig } from '@/common/utils/config';

const { Sider, Content } = Layout;

const ProtectedLayout = () => {
  const { user } = useAuth();
  const location = useLocation();
  const { pathname } = location;

  const permissions = useMemo(() => get(user, 'permissions', []), [user]);

  const getMenuItems = useCallback(
    (menus) => {
      const result = [];
      menus.forEach((menu) => {
        const item = { ...menu };
        if (item.children) {
          item.children = getMenuItems(item.children);
        }
        if (permissions.indexOf(item.key) > -1) {
          const path = item.key.split('.').join('/');
          item.label = <Link to={path}>{item.label}</Link>;
          result.push(item);
        }
      });
      return result;
    },
    [permissions]
  );

  const items = getMenuItems(menuItemsConfig);

  const defaultOpenKeys = useMemo(() => {
    const result = [];
    tranverseTree(items, (item) => {
      const { key } = item;
      if (!isLeafNode(item)) {
        result.push(key);
      }
    });
    return result;
  }, [items]);

  const selectedKeys = useMemo(() => {
    const paths = pathname.split('/').slice(1);
    const leafNodes = [];
    let path = paths.join('.');

    tranverseTree(items, (item) => {
      if (isLeafNode(item)) {
        leafNodes.push(item);
      }
    });
    if (!find(leafNodes, ['key', path])) {
      path = [path.split('.')[0], 'list'].join('.');
    }
    return [path];
  }, [pathname, items]);

  return (
    <Layout>
      <HeaderNav />
      <Layout>
        <Sider>
          <Menu
            defaultOpenKeys={defaultOpenKeys}
            mode="inline"
            selectedKeys={selectedKeys}
            items={items}
            className="dbr-sider-menu"
          />
        </Sider>
        <Content>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};
export default ProtectedLayout;
