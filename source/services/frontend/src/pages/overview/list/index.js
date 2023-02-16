/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-14 13:46:27
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-14 14:08:38
 * @FilePath: /huanghe/source/services/frontend/src/pages/overview/list/ServerList.js
 * @Description: 服务器列表页
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import qs from 'qs';
import api from '@/common/api';
import { purifyDeep } from '@/common/utils/helper';
// import JobsFilter from './JobsFilter';
import ServerListTable from './ServerListTable';

const ServerList = () => {
  const defaultFilters = useMemo(
    () => ({
      pageno: 1,
      pagesize: 10,
      sort: 'id:desc',
      filter: {
        username: null,
        role__name: 'all',
        project__code: 'all',
      },
    }),
    []
  );
  const [tableData, setTableData] = useState();
  const [loading, setLoading] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();

  const getFilters = useCallback(
    () => ({ ...defaultFilters, ...qs.parse(searchParams.toString()) }),
    [defaultFilters, searchParams]
  );

  const requestList = useCallback(
    async (args) => {
      const { loading = false, ...rest } = args;
      const params = purifyDeep({ ...getFilters(), ...rest });
      try {
        setLoading(loading);
        const { result } = await api.serverList(params);
        setTableData(result);
        setLoading(false);
      } catch (error) {
        console.log(error);
        setLoading(false);
      }
    },
    [getFilters]
  );

  const reload = (args) => {
    const filters = getFilters();
    const params = purifyDeep({ ...filters, ...args });
    // 手动同步Url
    setSearchParams(qs.stringify(params));
    requestList(params);
  };

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestList({ loading: true });
    // requestProjects();
    const filters = getFilters();
    setSearchParams(qs.stringify(filters));
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      reload();
    }, 3000);
    return () => {
      clearInterval(timer);
    };
  }, [searchParams]);

  const onPageNoChange = (pageno, pagesize) => {
    reload({ pageno, pagesize });
  };
  return (
    <div className="storages-list">
      <div className="dbr-table-container">
        <ServerListTable
          tableData={tableData}
          reload={reload}
          loading={loading}
          onPageNoChange={onPageNoChange}
        />
      </div>
    </div>
  );
};

export default ServerList;
