/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-01 15:53:49
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-01 18:40:15
 * @FilePath: /huanghe/source/services/frontend/src/pages/notebooks/detail/index.js
 * @Description: detail page
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { Col, Row, Tabs } from 'antd';
import { ChartMonitor, EventMonitor } from '@/common/components';
import { purifyDeep } from '@/common/utils/helper';
import api from '@/common/api';
import './index.less';

const NotebookDetail = () => {
  const [tableData, setTableData] = useState();
  const [loading, setLoading] = useState(false);

  const requestList = useCallback(async (args) => {
    const { loading = false, ...rest } = args;
    const params = purifyDeep({ ...rest });
    try {
      setLoading(loading);
      const { result } = await api.notebooksList(params); // to do
      setTableData(result);
      setLoading(false);
    } catch (error) {
      console.log(error);
      setLoading(false);
    }
  }, []);

  const reload = (args) => {
    const params = purifyDeep({ ...args });
    // 手动同步Url
    requestList(params);
  };

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestList({ loading: true });
  }, []);
  useEffect(() => {
    const timer = setInterval(() => {
      reload();
    }, 3000);
    return () => {
      clearInterval(timer);
    };
  }, []);

  const onPageNoChange = (pageno, pagesize) => {
    reload({ pageno, pagesize });
  };

  const onChange = (key) => {
    console.log(key);
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
          <Col span={6}>名称：hb-test-01</Col>
          <Col span={6}>项目：</Col>
          <Col span={6}>存储挂载：</Col>
          <Col span={6}>镜像：</Col>
          <Col span={6}>资源规格：</Col>
          <Col span={6}>创建人：</Col>
          <Col span={6}>创建时间：</Col>
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
