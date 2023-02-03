/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-01 15:53:49
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-03 11:42:07
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

  const defaultFilters = useMemo(
    () => ({
      pageno: 1,
      pagesize: 10,
      sort: 'update_at:desc',
      filter: {
        // username: null,
        // role__name: 'all',
        // project__code: 'all',
      },
    }),
    []
  );

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

  const requestEvent = useCallback(
    async (args) => {
      const { loading = false, ...rest } = args;
      const params = purifyDeep({ ...getFilters(), ...rest });
      try {
        setLoading(loading);
        const { result } = await api.notebooksDetailEvent(params);
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
        requestEvent({ loading: true });
        break;
    }
  };

  return (
    <div className="detail">
      <div className="detail-section">
        <Row gutter={[16, 24]}>
          <Col span={6} title={detailData?.name}>
            名称：{detailData?.name}
          </Col>
          <Col span={6} title={detailData?.project?.name}>
            项目：{detailData?.project?.name}
          </Col>
          <Col
            span={6}
            title={(() =>
              detailData?.hooks?.map((v) => v?.storage?.name || '-'))()}
          >
            存储挂载：
            {(() => detailData?.hooks?.map((v) => v?.storage?.name || '-'))()}
          </Col>
          <Col span={6} title={detailData?.image?.name}>
            镜像：{detailData?.image?.name}
          </Col>
          <Col span={6} title={detailData?.source}>
            资源规格：{detailData?.source}
          </Col>
          <Col span={6} title={detailData?.creator?.username}>
            创建人：{detailData?.creator?.username}
          </Col>
          <Col span={6} title={transformDate(detailData?.createdAt) || '-'}>
            创建时间：{transformDate(detailData?.createdAt) || '-'}
          </Col>
          <Col span={6}></Col>
        </Row>
      </div>
      <div className="dbr-table-container">
        <Tabs
          defaultActiveKey="chart-monitor"
          items={[
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
          ]}
          onChange={onChange}
        />
      </div>
    </div>
  );
};

export default NotebookDetail;
