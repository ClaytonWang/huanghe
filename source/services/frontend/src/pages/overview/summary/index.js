/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-01-31 15:07:28
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-15 10:51:47
 * @FilePath: /huanghe/source/services/frontend/src/pages/overview/summary/index.js
 * @Description: Overview Summary page
 */
import { useEffect, useState, useMemo, useRef } from 'react';
import { Select, Space, Row, Col } from 'antd';
import { CREATE, UPDATE, ADMIN } from '@/common/constants';
import { useAuth } from '@/common/hooks/useAuth';
import api from '@/common/api';
import './index.less';

const { Option } = Select;

const OverviewList = () => {
  const [projectsDatasource, setProjectsDatasource] = useState([]);
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

  const defaultProjects = useMemo(() => {
    if (projectsDatasource && projectsDatasource.length > 0) {
      return [projectsDatasource[0].id];
    }
  }, [projectsDatasource]);

  return (
    <div className="detail">
      <Row style={{ marginBottom: 10 }}>
        <Col span={12}>
          <Space>
            项目：
            <Select
              mode="multiple"
              allowClear
              style={{
                minWidth: 300,
              }}
              placeholder="请选择项目"
              defaultValue={defaultProjects}
              onChange={handleChange}
              options={projectsDatasource.map(({ id, name = '-' }) => ({
                label: name,
                value: id,
              }))}
            />
          </Space>
        </Col>
      </Row>
      <div className="detail-section"></div>
      <div className="detail-section"></div>
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
