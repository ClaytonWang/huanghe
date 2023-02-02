/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-01 15:53:49
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-02 14:24:08
 * @FilePath: /huanghe/source/services/frontend/src/pages/notebooks/detail/index.js
 * @Description: detail page
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Col, Row, Tabs } from 'antd';
import { ChartMonitor, EventMonitor } from '@/common/components';
import { purifyDeep } from '@/common/utils/helper';
import { transformDate } from '@/common/utils/helper';
import api from '@/common/api';
import qs from 'qs';
import './index.less';

const NotebookDetail = () => {
  const [tableData, setTableData] = useState([]);
  const [detailData, setDetailData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();

  const defaultFilters = useMemo(() => ({}), []);

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
        const { result } = await api.notebooksDetail(params);
        setDetailData(result);
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
    const filters = getFilters();
    setSearchParams(qs.stringify(filters));
  }, []);

  // useEffect(() => {
  //   const timer = setInterval(() => {
  //     reload();
  //   }, 3000);
  //   return () => {
  //     clearInterval(timer);
  //   };
  // }, [searchParams]);

  const onPageNoChange = (pageno, pagesize) => {
    reload({ pageno, pagesize });
  };

  const onChange = (key) => {
    // eslint-disable-next-line default-case
    switch (key) {
      case 'event-monitor':
        setTableData({
          total: 1,
          data: [
            {
              id: '1',
              status: '胡彦斌',
              time: '2023-01-31T10:58:25.030773',
              name: '西湖区湖底公园1号',
            },
          ],
        });
        break;
    }
  };

  const items = [
    {
      key: 'chart-monitor',
      label: `监控`,
      children: <ChartMonitor />,
    },
    {
      key: 'event-monitor',
      label: `事件`,
      children: (
        <EventMonitor
          onPageNoChange={onPageNoChange}
          tableData={tableData}
          reload={reload}
          loading={loading}
        />
      ),
    },
  ];
  return (
    <div className="detail">
      <div className="detail-section">
        <Row gutter={[16, 24]}>
          <Col span={6}>名称：{detailData?.name}</Col>
          <Col span={6}>项目：{detailData?.project?.name}</Col>
          <Col span={6}>
            存储挂载：
            {(() => detailData?.hooks?.map((v) => v?.storage?.name || '-'))()}
          </Col>
          <Col span={6}>镜像：{detailData?.image?.name}</Col>
          <Col span={6}>资源规格：{detailData?.source}</Col>
          <Col span={6}>创建人：{detailData?.creator?.username}</Col>
          <Col span={6}>
            创建时间：{transformDate(detailData?.createdAt) || '-'}
          </Col>
          <Col span={6}></Col>
        </Row>
      </div>
      <div className="dbr-table-container">
        <Tabs
          defaultActiveKey="chart-monitor"
          items={items}
          onChange={onChange}
        />
      </div>
    </div>
  );
};

export default NotebookDetail;
