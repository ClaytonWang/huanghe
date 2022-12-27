/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-11-29 10:59:16
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-09 17:05:04
 * @Description Authenticate user info before render component
 */
import { Link, Outlet, useNavigate } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import { get, find } from 'lodash';
import { useCallback, useEffect, useMemo } from 'react';
import Icon from '@ant-design/icons';
import HeaderNav from '@/common/components/HeaderNav';
import { useAuth } from '@/common/hooks/useAuth';
import { tranverseTree, isLeafNode } from '@/common/utils/helper';
import { menuItemsConfig } from '@/common/utils/config';
import Icons from '@/common/components/Icon';
import './index.less';

const { Sider, Content } = Layout;

const ProtectedLayout = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

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
          if (item.icon) {
            item.icon = <Icon component={Icons[item.icon]} />;
          }
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
    if (items.length > 0) {
      tranverseTree(items, (item) => {
        const { key } = item;
        if (!isLeafNode(item)) {
          result.push(key);
        }
      });
    }
    return result;
  }, [items]);

  const selectedKeys = useMemo(() => {
    const result = [];
    if (items.length > 0 && defaultOpenKeys.length > 0) {
      const firstMenu = defaultOpenKeys[0];
      const item = find(items, ['key', firstMenu]);
      const pathname = item.children[0].key;
      result.push(pathname);
    }
    return result;
  }, [defaultOpenKeys, items]);

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    // if location is empty, auto direct to first submenu; else maintain;
    const pathname = (selectedKeys.length > 0 && selectedKeys[0]) || '';
    const path = pathname.split('.').join('/');
    navigate(path);
  }, []);

  return (
    <Layout className="protected-layout">
      <HeaderNav />
      <Layout>
        <Sider>
          <Menu
            defaultOpenKeys={defaultOpenKeys}
            mode="inline"
            defaultSelectedKeys={selectedKeys}
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
