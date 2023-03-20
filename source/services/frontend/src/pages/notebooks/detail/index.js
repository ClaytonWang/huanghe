/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-01 15:53:49
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-03-20 14:41:02
 * @FilePath: /huanghe/source/services/frontend/src/pages/notebooks/detail/index.js
 * @Description: detail page
 */
import { useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Col,
  Row,
  Card,
  Space,
  Skeleton,
  Dropdown,
  Tooltip,
  Spin,
  message,
  Modal,
  DatePicker,
  Button,
  Typography,
} from 'antd';
import Icon, { InfoCircleOutlined } from '@ant-design/icons';
import { GrafanaComponent, EventList, AuthButton } from '@/common/components';
import { get } from 'lodash';

import { join, purifyDeep, transformDate } from '@/common/utils/helper';
import api from '@/common/api';
import qs from 'qs';
import { NOTEBOOK_ACTION, START, STOP, UPDATE } from '@/common/constants';
import Icons from '@/common/components/Icon';
import { useContextProps } from '@/common/hooks/RoutesProvider';
import moment from 'moment';

import './index.less';

const { RangePicker } = DatePicker;
const DATE_FORMAT = 'YYYY/MM/DD HH:mm:ss';

const NotebookDetail = () => {
  const { id: notebookId } = useParams();
  const [eventTableData, setEventTableData] = useState({});
  const [detailData, setDetailData] = useState(null);
  const [currTab, setCurrTab] = useState('chart');
  const [dateRange, setDateRange] = useState({
    from: null, // 默认1小时
    to: null,
  });
  const [loading, setLoading] = useState(false);
  const [eventLoading, setEventLoading] = useState(false);
  const setContextProps = useContextProps();
  const navigate = useNavigate();
  const defaultFilters = {
    pageno: 1,
    pagesize: 2,
  };

  const rangePresets = useMemo(
    () => [
      {
        label: 'Last 7 Days',
        value: [moment().add(-7, 'd'), moment()],
      },
      {
        label: 'Last 14 Days',
        value: [moment().add(-14, 'd'), moment()],
      },
      {
        label: 'Last 30 Days',
        value: [moment().add(-30, 'd'), moment()],
      },
      {
        label: 'Last 90 Days',
        value: [moment().add(-90, 'd'), moment()],
      },
    ],
    []
  );

  const requestList = async (args) => {
    const { loading = false, ...rest } = args;
    const params = purifyDeep({ ...rest });
    try {
      setLoading(loading);
      const { result } = await api.notebooksDetail(params);
      setDetailData(result);
      setLoading(false);
    } catch (error) {
      console.log(error);
      setLoading(false);
    }
  };

  const requestEvent = async (args) => {
    const { loading = false, ...rest } = args;
    const params = purifyDeep({ ...defaultFilters, ...rest });
    try {
      setEventLoading(loading);
      const { result } = await api.notebooksDetailEvent(params);
      setEventTableData({
        ...defaultFilters,
        ...result,
      });
    } catch (error) {
      console.log(error);
    } finally {
      setEventLoading(false);
    }
  };

  /* eslint-disable react-hooks/exhaustive-deps */
  const reload = async (args) => {
    const params = purifyDeep({ ...args });
    requestList(params);
  };

  const handleStartClicked = async (record) => {
    try {
      const { id } = record;
      await api.notebooksListAction({ id, action: NOTEBOOK_ACTION[START] });
      message.success('已触发启动！');
    } catch (error) {
      console.log(error);
    }
  };
  const onStop = async (record) => {
    try {
      const { id } = record;
      await api.notebooksListAction({ id, action: NOTEBOOK_ACTION[STOP] });
      message.success('已触发停止！');
    } catch (error) {
      console.log(error);
    }
  };

  const handleStopClicked = (record) => {
    Modal.confirm({
      title: '可能会导致数据丢失，是否要停止该Job服务？',
      okText: '停止',
      cancelText: '取消',
      onOk: () => {
        onStop(record);
      },
    });
  };

  const handleEditClicked = (values) => {
    navigate('/notebooks/list/update', {
      state: {
        params: values,
        type: UPDATE,
      },
    });
  };

  const deleteNotebook = async (record) => {
    const { id } = record;
    try {
      await api.notebooksListDelete({ id });
      message.success('删除Notebook成功！');
      navigate('/notebooks/list');
    } catch (error) {
      console.log(error);
    }
  };

  const handleDelete = (record) => {
    Modal.confirm({
      title: '确定要删除该Notebook吗？',
      okText: '删除',
      okType: 'danger',
      cancelText: '取消',
      onOk: () => {
        deleteNotebook(record);
      },
    });
  };
  const handleConfigInfoClicked = () => {
    const sshConfig = detailData?.ssh;
    Modal.info({
      title: 'SSH配置信息',
      content: (
        <div className="ssh-config">
          <p>账号：{sshConfig?.account}</p>
          <p>密码：{sshConfig?.password}</p>
          <p>地址：{sshConfig?.address}</p>
        </div>
      ),
    });
  };

  const onPageNoChange = (pageno, pagesize) => {
    const params = purifyDeep({ pageno, pagesize });
    requestEvent(params);
  };

  const onTabChange = (key) => {
    setCurrTab(key);
    // eslint-disable-next-line default-case
    switch (key) {
      case 'event':
        // requestEvent({ loading: true, id: notebookId });
        break;
    }
  };

  const onRangeChange = (dates) => {
    if (dates) {
      setDateRange({ from: dates[0]?.valueOf(), to: dates[1]?.valueOf() });
    } else {
      console.log('Clear');
    }
  };

  const findTimeRange = (obj) => {
    if (!obj) return {};
    const urls = Object.values(obj);
    for (let i = 0; i < urls.length; i++) {
      let { from = null, to = null } =
        urls[i].split('?').length > 0 && qs.parse(urls[i].split('?')[1]);
      if (from && to) {
        return { from: Number(from), to: Number(to) };
      }
    }
    return {};
  };

  const operations = useMemo(() => {
    if (currTab === 'event') return null;
    console.log(dateRange);
    return (
      <RangePicker
        allowClear={false}
        presets={rangePresets}
        showTime
        format={DATE_FORMAT}
        onChange={onRangeChange}
        placement="bottomRight"
        value={[
          moment(dateRange.from) || moment().add(-1, 'h'),
          moment(dateRange.to) || moment(),
        ]}
      />
    );
  }, [currTab, rangePresets, dateRange]);

  const contentList = {
    chart: <GrafanaComponent urls={detailData?.grafana} />,
    event: (
      <EventList
        onPageNoChange={onPageNoChange}
        eventTableData={eventTableData}
        reload={reload}
        loading={eventLoading}
      />
    ),
  };

  useEffect(() => {
    const timer = setInterval(() => {
      reload();
    }, 3000);
    return () => {
      clearInterval(timer);
    };
  }, [reload]);

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestList({ loading: true, id: notebookId });
    requestEvent({ loading: true, id: notebookId });
  }, []);

  useEffect(() => {
    if (detailData != null) {
      const { from = null, to = null } = findTimeRange(detailData?.grafana);
      setDateRange({
        from: transformDate(from, DATE_FORMAT),
        to: transformDate(to, DATE_FORMAT),
      });
    }
    setContextProps({
      handleStartClicked,
      handleStopClicked,
      handleEditClicked,
      handleDelete,
      detail: detailData,
      loading,
      setLoading,
    });
  }, [detailData]);

  return (
    <div className="notebooks-detail">
      <div className="detail-section">
        <Row gutter={[16, 24]}>
          {loading ? (
            <Skeleton active />
          ) : (
            <>
              <Col span={6} title={detailData?.name}>
                名称：{detailData?.name}
              </Col>
              <Col span={6} title={detailData?.project?.name}>
                项目：{detailData?.project?.name}
              </Col>
              <Col
                span={6}
                title={join(
                  detailData?.hooks,
                  '\n',
                  (v) => `挂载盘：${v?.storage?.name}\n路径：${v?.path}` || '-'
                )}
              >
                存储挂载：
                {join(detailData?.hooks, ',', (v) => v?.storage?.name || '-')}
              </Col>
              <Col span={6} title={detailData?.image?.name}>
                <Tooltip title={detailData?.image?.name}>
                  <Typography.Text
                    copyable={{
                      tooltips: false,
                      text: detailData?.image?.name,
                    }}
                  >
                    <span className="overflow">
                      镜像：{detailData?.image?.name}
                    </span>
                  </Typography.Text>
                </Tooltip>
              </Col>
              <Col span={6} title={detailData?.source}>
                资源规格：{detailData?.source}
              </Col>
              <Col span={6} title="SSH远程开发">
                SSH远程开发
                <Tooltip
                  title={
                    <span>
                      详细说明请参考
                      <Button
                        type="link"
                        href="https://digital-brain.feishu.cn/docx/IzMPd7NCYoSTYjxJNDTcLC1HnCg"
                      >
                        使用手册
                      </Button>
                    </span>
                  }
                >
                  <InfoCircleOutlined />
                </Tooltip>
                :
                <Button
                  type="link"
                  style={{ marginLeft: 5 }}
                  onClick={handleConfigInfoClicked}
                >
                  查看配置信息
                </Button>
              </Col>
              <Col span={6} title={detailData?.creator?.username}>
                创建人：{detailData?.creator?.username}
              </Col>
              <Col span={6} title={transformDate(detailData?.createdAt) || '-'}>
                创建时间：{transformDate(detailData?.createdAt) || '-'}
              </Col>
              <Col span={6}></Col>
            </>
          )}
        </Row>
      </div>
      <div className="monitor-container">
        <Card
          activeTabKey={currTab}
          tabBarExtraContent={operations}
          tabList={[
            {
              key: 'chart',
              tab: '监控',
            },
            {
              key: 'event',
              tab: '事件',
            },
          ]}
          onTabChange={onTabChange}
        >
          {contentList[currTab]}
        </Card>
      </div>
    </div>
  );
};

NotebookDetail.context = (props = {}) => {
  const {
    handleStartClicked,
    handleStopClicked,
    handleEditClicked,
    handleDelete,
    detail,
  } = props;
  const statusName = get(detail, 'status.name');
  const statusDesc = get(detail, 'status.desc');
  const menuProps = {
    items: [
      {
        label: (
          <AuthButton
            required="notebooks.list.edit"
            type="text"
            onClick={() => {
              handleEditClicked(detail);
            }}
            condition={[
              () => ['stopped'].indexOf(statusName) > -1,
              (user) =>
                get(detail, 'creator.username') === get(user, 'username'),
            ]}
          >
            编辑
          </AuthButton>
        ),
        key: 'edit',
      },
      {
        label: (
          <AuthButton
            required="notebooks.list.edit"
            type="text"
            onClick={() => {
              handleDelete(detail);
            }}
            condition={[
              () => ['stopped', 'error'].indexOf(statusName) > -1,
              (user) =>
                get(detail, 'creator.username') === get(user, 'username'),
            ]}
          >
            删除
          </AuthButton>
        ),
        key: 'delete',
      },
    ],
  };
  return (
    <Space>
      {(() => {
        if (!statusName) return null;
        let icon = (
          <Icon
            style={{ fontSize: 18, marginRight: 5 }}
            component={Icons[statusName]}
          />
        );
        if (/^(stop|start|pending)$/.test(statusName)) {
          icon = (
            <Spin
              indicator={
                <Icon
                  style={{ fontSize: 16, marginRight: 5 }}
                  component={Icons[statusName]}
                  spin
                  rotate={(/pending/.test(statusName) && 180) || 0}
                />
              }
            />
          );
        }
        return (
          <label>
            <Tooltip title={statusDesc}>{icon}</Tooltip>
            {statusDesc}
          </label>
        );
      })()}
      <Dropdown.Button menu={menuProps} trigger="click">
        {statusName === 'stopped' && (
          <AuthButton
            required="notebooks.list.edit"
            type="text"
            onClick={() => {
              handleStartClicked(detail);
            }}
            condition={[
              (user) =>
                get(detail, 'creator.username') === get(user, 'username'),
            ]}
          >
            启动
          </AuthButton>
        )}
        {statusName !== 'stopped' && (
          <AuthButton
            required="notebooks.list.edit"
            type="text"
            style={(() => {
              if (statusName === 'error') {
                return { color: '#00000040' };
              }
            })()}
            onClick={() => {
              handleStopClicked(detail);
            }}
            condition={[
              () => ['error', 'stop'].indexOf(statusName) < 0,
              (user) =>
                get(detail, 'creator.username') === get(user, 'username'),
            ]}
          >
            停止
          </AuthButton>
        )}
      </Dropdown.Button>
      <AuthButton
        required="notebooks.list"
        type="primary"
        onClick={() => {
          const { url } = detail;
          window.open(url);
        }}
        condition={[
          () => ['running'].indexOf(statusName) > -1,
          (user) => get(detail, 'creator.username') === get(user, 'username'),
        ]}
      >
        打开
      </AuthButton>
    </Space>
  );
};

NotebookDetail.path = '/notebooks/list/detail';

export default NotebookDetail;
