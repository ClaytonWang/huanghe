/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-01-31 15:07:28
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-15 18:18:39
 * @FilePath: /huanghe/source/services/frontend/src/pages/overview/summary/index.js
 * @Description: Overview Summary page
 */
import { useEffect, useState, useMemo, useRef } from 'react';
import { Select, Space, Row, Col, Card, Statistic } from 'antd';
import { CREATE, UPDATE, ADMIN } from '@/common/constants';
import { useAuth } from '@/common/hooks/useAuth';
import api from '@/common/api';
import CountUp from 'react-countup';
import './index.less';

const { Option } = Select;

const formatter = (value) => <CountUp end={value} separator="," />;

const StatisticCard = ({ title, total = 0, run = 0, onClick }) => (
  <Card.Grid style={{ width: '100%', padding: 15 }}>
    <Row justify="space-between">
      <Col span={12} style={{ fontWeight: 'bold' }}>
        {title}
      </Col>
      <Col span={6} offset={6} style={{ textAlign: 'right' }}>
        <a onClick={onClick}>查看详情</a>
      </Col>
    </Row>
    <Row style={{ marginTop: 10 }}>
      <Col span={12}>
        <Statistic value={total} formatter={formatter} />
        任务数量
      </Col>
      <Col span={12}>
        <Statistic value={run} formatter={formatter} />
        运行中
      </Col>
    </Row>
  </Card.Grid>
);

const SourceStatisticCard = ({
  title,
  occupied = 0,
  used = 0,
  occupied_rate = 0,
}) => (
  <Card.Grid style={{ width: '100%', padding: 15 }}>
    <Row>
      <Col span={24} style={{ fontWeight: 'bold' }}>
        {title}
      </Col>
    </Row>
    <Row style={{ marginTop: 10 }}>
      <Col span={8}>
        <Statistic value={occupied} formatter={formatter} suffix="C" />
        已占用
      </Col>
      <Col span={8} style={{ textAlign: 'center' }}>
        <Statistic value={used} formatter={formatter} suffix="C" />
        已使用
      </Col>
      <Col span={8} style={{ textAlign: 'right' }}>
        <Statistic value={occupied_rate} formatter={formatter} suffix="%" />
        占用率
      </Col>
    </Row>
  </Card.Grid>
);

const OverviewList = () => {
  const [projectsDatasource, setProjectsDatasource] = useState([]);
  const [selectedProj, setSelectedProj] = useState([]);
  const { user } = useAuth();

  const options = [];
  for (let i = 10; i < 36; i++) {
    options.push({
      label: i.toString(36) + i,
      value: i.toString(36) + i,
    });
  }

  const handleChange = (value) => {
    console.log(`selected ${value}`);
    setSelectedProj(value);
  };

  const requestProjects = async () => {
    try {
      if (user.role.name === ADMIN) {
        const { result } = await api.bamProjectsList();
        setProjectsDatasource(result.data);
      } else {
        // 除超级管理员角色，其他项目列表返回自己所属项目
        setProjectsDatasource(user?.projects ?? []);
      }
    } catch (error) {
      console.log(error);
    }
  };

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestProjects();
  }, []);

  useEffect(() => {
    if (projectsDatasource && projectsDatasource.length > 0) {
      const _data = projectsDatasource.map(({ id }) => id);
      setSelectedProj(_data);
    }
  }, [projectsDatasource]);

  return (
    <div className="detail">
      <Row style={{ marginBottom: 10 }}>
        <Col span={24}>
          <Space>
            项目：
            <Select
              mode="multiple"
              maxTagCount="responsive"
              allowClear
              style={{
                minWidth: 400,
                maxWidth: 800,
              }}
              placeholder="请选择项目"
              value={selectedProj}
              onChange={handleChange}
              options={projectsDatasource.map(({ id, name = '-' }) => ({
                label: name,
                value: id,
              }))}
            />
          </Space>
        </Col>
      </Row>
      <Card size="small" title="开发统计">
        <Row gutter={10}>
          <Col span={6}>
            <StatisticCard title="Notebooke" />
          </Col>
          <Col span={6}>
            <StatisticCard title="Job" />
          </Col>
        </Row>
      </Card>
      <br />
      <Card size="small" title="资源统计">
        <Row gutter={10}>
          <Col span={6}>
            <SourceStatisticCard title="CPU" />
          </Col>
          <Col span={6}>
            <SourceStatisticCard title="GPU" />
          </Col>
          <Col span={6}>
            <SourceStatisticCard title="内存" />
          </Col>
          <Col span={6}>
            <SourceStatisticCard title="存储" />
          </Col>
        </Row>
      </Card>
    </div>
  );
};

// const grafana = `https://grafana.digitalbrain.cn:32443/d/l_ZkLT5Vz
// /ji-qun-jian-kong?orgId=1&from=now-3h&to=now&theme=light&kiosk=tv&refresh=10s `;

// return (
//   <div className="overview-list">
//     <iframe name="iframe" className="content" src={grafana} />
//   </div>
// );

export default OverviewList;
