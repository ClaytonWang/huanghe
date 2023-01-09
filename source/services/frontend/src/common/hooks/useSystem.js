/**
 * @description system hook, provide global cached data
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  useCallback,
} from 'react';
import { Spin } from 'antd';
import api from '@/common/api';
import { useAuth } from './useAuth';

const SystemContext = createContext();
export const SystemProvider = ({ children }) => {
  const { token, requestAccount } = useAuth();
  const [organizations, setOrganizations] = useState([]);
  const [renderChildren, setRenderChildren] = useState(false);

  const loadAccount = async () => {
    try {
      await requestAccount();
      setRenderChildren(true);
    } catch (error) {
      console.log(error);
      setRenderChildren(false);
    }
  };

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    loadAccount();
  }, [token]);

  // 获取组织列表
  const loadOrganizations = useCallback(async () => {
    try {
      const data = await api.settingsOrganizationsList();
      // TODO: check if need to transform id:xx,name:xx to value:xx,name:xxx
      setOrganizations(data.result);
      return Promise.resolve(data.result);
    } catch (error) {
      console.log(error);
      return Promise.reject(new Error('load organizations failed.'));
    }
  }, []);

  const renderLoading = () => (
    <Spin
      size="large"
      tip="Loading..."
      style={{ width: '100%', height: '100%' }}
    />
  );

  const value = useMemo(
    () => ({
      organizations,
      loadOrganizations,
    }),
    [organizations, loadOrganizations]
  );

  return (
    <SystemContext.Provider value={value}>
      {(renderChildren && children) || renderLoading()}
    </SystemContext.Provider>
  );
};

export const useSystem = () => useContext(SystemContext);
