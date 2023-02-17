/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-01-31 15:07:28
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-17 11:21:35
 * @FilePath: /huanghe/source/services/frontend/src/pages/overview/summary/index.js
 * @Description: Overview Summary page
 */
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Select, Space, Row, Col, Card, Statistic, Skeleton } from 'antd';
import { DownOutlined, UpOutlined, RightOutlined } from '@ant-design/icons';
import { ADMIN } from '@/common/constants';
import { useAuth } from '@/common/hooks/useAuth';
import api from '@/common/api';
import CountUp from 'react-countup';
import './index.less';

const formatter = (value) => (
  <CountUp end={value} separator="," duration="0.5" />
);

const StatisticCard = ({ title, total = 0, run = 0, to }) => (
  <Card.Grid style={{ width: '100%', padding: 15 }}>
    <Row justify="space-between">
      <Col span={12} style={{ fontWeight: 'bold' }}>
        {title}
      </Col>
      <Col span={12} style={{ textAlign: 'right' }}>
        <Link to={to}>
          查看详情
          <RightOutlined />
        </Link>
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
  suffix = 'C',
}) => (
  <Card.Grid style={{ width: '100%', padding: 15 }}>
    <Row>
      <Col span={24} style={{ fontWeight: 'bold' }}>
        {title}
      </Col>
    </Row>
    <Row style={{ marginTop: 10 }}>
      <Col span={8}>
        <Statistic value={occupied} formatter={formatter} suffix={suffix} />
        已占用
      </Col>
      <Col span={8} style={{ textAlign: 'center' }}>
        <Statistic value={used} formatter={formatter} suffix={suffix} />
        已使用
      </Col>
      <Col span={8} style={{ textAlign: 'right' }}>
        <Statistic value={occupied_rate} formatter={formatter} suffix="%" />
        占用率
      </Col>
    </Row>
  </Card.Grid>
);

const OverviewChartMonitor = () => {
  const grafana = `https://grafana.digitalbrain.cn:32443/d/l_ZkLT5Vz
/ji-qun-jian-kong?orgId=1&from=now-3h&to=now&theme=light&kiosk=tv&refresh=10s`;

  return (
    <div className="overview-list">
      <iframe name="iframe" className="content" src={grafana} />
    </div>
  );
};

const OverviewList = () => {
  const [projectsDatasource, setProjectsDatasource] = useState([]);
  const [selectedProj, setSelectedProj] = useState([]);
  const [tasksData, setTasksData] = useState([]);
  const [sourceData, setSourceData] = useState([]);
  const [loading, setLoading] = useState(false);

  const [open, setOpen] = useState(false);
  const { user } = useAuth();

  const options = [];
  for (let i = 10; i < 36; i++) {
    options.push({
      label: i.toString(36) + i,
      value: i.toString(36) + i,
    });
  }

  const handleChange = (value) => {
    setSelectedProj(value);
  };

  const requestProjects = async () => {
    try {
      setLoading(true);
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

  const requestTasks = async (project) => {
    try {
      setLoading(true);
      const params = { project };
      const { result } = await api.serverTask(params);
      setTasksData(result);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  const requestSource = async (project) => {
    setLoading(true);
    try {
      setLoading(true);
      const params = { project };
      const { result } = await api.serverSource(params);
      setSourceData(result);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
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

  useEffect(() => {
    if (selectedProj && selectedProj.length > 0) {
      requestTasks(selectedProj);
      requestSource(selectedProj);
    }
  }, [selectedProj]);

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
              loading={loading}
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
          {loading && <Skeleton active />}
          {tasksData?.map(({ name = '-', total = 0, running = 0 }) => (
            <Col key={name} span={6}>
              <StatisticCard
                title={name}
                total={total}
                run={running}
                to={`/${name.toLocaleLowerCase()}s/list`}
              />
            </Col>
          ))}
        </Row>
      </Card>
      <br />
      <Card size="small" title="资源统计">
        <Row gutter={10}>
          {loading && <Skeleton active />}
          {sourceData?.map(
            ({ name = '-', occupied = 0, occupiedRate = 0, used = 0 }) => {
              let suffix = 'T';
              if (name === 'CPU' || name === 'GPU') {
                suffix = 'C';
              }
              return (
                <Col key={name} span={6}>
                  <SourceStatisticCard
                    title={name}
                    occupied={occupied}
                    occupied_rate={occupiedRate * 100}
                    used={used}
                    suffix={suffix}
                  />
                </Col>
              );
            }
          )}
        </Row>
        <Row style={{ marginTop: 15 }}>
          <Col span={24}>
            <a
              onClick={() => {
                setOpen(!open);
              }}
            >
              {open ? '收起' : '展开'}
              {open ? <UpOutlined /> : <DownOutlined />}
            </a>
          </Col>
        </Row>
        {open ? (
          <Row>
            <Col span={24}>
              <OverviewChartMonitor />
            </Col>
          </Row>
        ) : null}
      </Card>
    </div>
  );
};

export default OverviewList;
