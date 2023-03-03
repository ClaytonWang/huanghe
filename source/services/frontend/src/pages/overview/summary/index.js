/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-01-31 15:07:28
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-03-03 16:06:52
 * @FilePath: /huanghe/source/services/frontend/src/pages/overview/summary/index.js
 * @Description: Overview Summary page
 */
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import CountUp from 'react-countup';
import {
  Select,
  Space,
  Row,
  Col,
  Card,
  Statistic,
  Skeleton,
  Empty,
} from 'antd';
import { RightOutlined } from '@ant-design/icons';
import { ADMIN } from '@/common/constants';
import { useAuth } from '@/common/hooks/useAuth';
import api from '@/common/api';
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
  const [selectedProject, setSelectedProject] = useState([]);
  const [tasksData, setTasksData] = useState([]);
  const [loading, setLoading] = useState(false);

  const { user } = useAuth();

  const handleChange = (value) => {
    setSelectedProject(value);
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
    } finally {
      setLoading(false);
    }
  };

  const requestTasks = async (project) => {
    try {
      const params = { project };
      const { result } = await api.serverTask(params);
      setTasksData(result);
      return Promise.resolve();
    } catch (error) {
      console.log(error);
      return Promise.reject(error);
    }
  };

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestProjects();
  }, []);

  useEffect(() => {
    if (projectsDatasource && projectsDatasource.length > 0) {
      const _data = projectsDatasource.map(({ id }) => id);
      setSelectedProject(_data);
    }
  }, [projectsDatasource]);

  useEffect(() => {
    if (selectedProject && selectedProject.length >= 0) {
      setLoading(true);
      const promises = [requestTasks].map((fn) => fn(selectedProject));
      Promise.all(promises)
        .then(() => {
          setLoading(false);
        })
        .catch(() => {
          setLoading(false);
        });
    }
  }, [selectedProject]);

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
              value={selectedProject}
              onClear={() => handleChange([])}
              onChange={handleChange}
              options={projectsDatasource.map(({ id, name = '-' }) => ({
                label: name,
                value: id,
              }))}
            />
          </Space>
        </Col>
      </Row>
      <Card title="开发统计">
        <Row gutter={10}>
          {loading ? (
            <Skeleton active />
          ) : (
            (tasksData?.length > 0 &&
              tasksData.map(({ name = '-', total = 0, running = 0 }) => (
                <Col key={name} span={6}>
                  <StatisticCard
                    title={name}
                    total={total}
                    run={running}
                    to={`/${name.toLocaleLowerCase()}s/list`}
                  />
                </Col>
              ))) || (
              <Empty
                image={Empty.PRESENTED_IMAGE_SIMPLE}
                style={{ width: '100%' }}
              />
            )
          )}
        </Row>
      </Card>
      <br />
      <Card title="资源统计">
        <Row>
          <Col span={24}>
            <OverviewChartMonitor />
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default OverviewList;
