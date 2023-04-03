/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-01 15:53:49
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-04-03 16:07:54
 * @FilePath: /huanghe/source/services/frontend/src/pages/jobs/detail/index.js
 * @Description: detail page
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Col,
  Card,
  Row,
  Space,
  Skeleton,
  Dropdown,
  Tooltip,
  Spin,
  message,
  Modal,
  DatePicker,
  Typography,
} from 'antd';
import Icon from '@ant-design/icons';
import {
  GrafanaComponent,
  EventList,
  AuthButton,
  Auth,
} from '@/common/components';
import { get, pickBy } from 'lodash';

import {
  purifyDeep,
  transformDate,
  getStatusName,
  join,
  sequencePromise,
} from '@/common/utils/helper';
import api from '@/common/api';
import qs from 'qs';
import moment from 'moment';
import {
  JOB_ACTION,
  START,
  STOP,
  UPDATE,
  DEBUG,
  COPY,
} from '@/common/constants';
import Icons from '@/common/components/Icon';
import { useContextProps } from '@/common/hooks/RoutesProvider';

import './index.less';

const { RangePicker } = DatePicker;

const JobDetail = () => {
  const { id: jobId } = useParams();
  const [eventTableData, setEventTableData] = useState([]);
  const [detailData, setDetailData] = useState(null);
  const [currTab, setCurrTab] = useState(null);
  const [grafanaSource, setGrafanaSource] = useState({});
  const [loggingSource, setLoggingSource] = useState({});
  const [dateRange, setDateRange] = useState({
    from: moment().add(-1, 'h'), // 默认1小时
    to: moment(),
  });
  const [logRange] = useState({
    from: moment().add(-1, 'h'), // 默认1小时
    to: moment(),
  });
  const [loading, setLoading] = useState(false);
  const setContextProps = useContextProps();
  const navigate = useNavigate();

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

  const requestList = useCallback(async (args) => {
    const { loading = false, ...rest } = args;
    const params = purifyDeep({ ...rest });
    try {
      setLoading(loading);
      const { result } = await api.jobDetail(params);
      setDetailData(result);
      setLoading(false);
      return Promise.resolve(result);
    } catch (error) {
      console.log(error);
      setLoading(false);
    }
  }, []);

  const requestEvent = useCallback(
    async (args) => {
      const { pageno, pagesize, ...rest } = args;
      const params = { pageno, pagesize, ...rest };
      try {
        setLoading(loading);
        const { result } = await api.jobDetailEvent(params);
        setEventTableData({
          ...result,
          pageno,
          pagesize,
        });
        setLoading(false);
      } catch (error) {
        console.log(error);
        setLoading(false);
      }
    },
    [loading]
  );

  const reload = useCallback(
    (args) => {
      const params = purifyDeep({ ...args });
      requestList({ ...params, id: jobId });
    },
    [jobId, requestList]
  );

  const handleStartClicked = async (record) => {
    try {
      const { id } = record;
      await api.jobListAction({ id, action: JOB_ACTION[START] });
      message.success('已触发启动！');
    } catch (error) {
      console.log(error);
    }
  };
  const onStop = async (record) => {
    try {
      const { id } = record;
      await api.jobListAction({ id, action: JOB_ACTION[STOP] });
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
    const { id } = values;
    navigate(`/jobs/list/update/${id}`, {
      state: {
        params: values,
        type: UPDATE,
      },
    });
  };

  const handleCopyClicked = (values) => {
    navigate('/jobs/list/copy', {
      state: {
        params: values,
        type: COPY,
      },
    });
    console.log('copy clicked');
  };

  const deleteJob = async (record) => {
    const { id } = record;
    try {
      await api.jobListDelete({ id });
      message.success('删除Job服务成功！');
      navigate('/jobs/list');
    } catch (error) {
      console.log(error);
    }
  };

  const handleDeleteClicked = (record) => {
    Modal.confirm({
      title: '确定要删除该Job服务吗？',
      okText: '删除',
      okType: 'danger',
      cancelText: '取消',
      onOk: () => {
        deleteJob(record);
      },
    });
  };

  const onPageNoChange = useCallback(
    (pageno, pagesize) => {
      requestEvent({ id: jobId, pageno, pagesize });
    },
    [jobId, requestEvent]
  );

  const onTabChange = (key) => {
    setCurrTab(key);
  };

  const initialData = (data) => {
    const { grafana = {}, loggingUrl = {} } = data;
    setGrafanaSource(grafana);
    setLoggingSource(loggingUrl);
    const url = Object.values(pickBy(grafana, (value) => value))[0];
    const params = url?.split('?')[1] && qs.parse(url.split('?')[1]);
    onRangeChange([moment(params.from), moment(params.to)]);
    return Promise.resolve();
  };

  const onRangeChange = (dates) => {
    if (dates) {
      setDateRange({ from: dates[0]?.valueOf(), to: dates[1]?.valueOf() });
    } else {
      console.log('Clear');
    }
  };

  const operations = useMemo(() => {
    const from = moment(dateRange.from);
    const to = moment(dateRange.to);

    const dateFormat = 'YYYY/MM/DD HH:mm:ss';
    if (currTab === 'chart') {
      return (
        <RangePicker
          allowClear={false}
          showTime
          format={dateFormat}
          onChange={onRangeChange}
          placement="bottomRight"
          defaultValue={[moment(from, dateFormat), moment(to, dateFormat)]}
        />
      );
    }

    if (currTab === 'log') {
      return null;
    }
    return null;
  }, [currTab, dateRange.from, dateRange.to]);

  const contentList = useMemo(
    () => [
      {
        name: 'chart',
        component: (
          <GrafanaComponent urls={grafanaSource} dateRange={dateRange} />
        ),
      },
      {
        name: 'event',
        component: (
          <EventList
            onPageNoChange={onPageNoChange}
            tableData={eventTableData}
            reload={reload}
            loading={loading}
          />
        ),
      },
      {
        name: 'log',
        component: (
          <GrafanaComponent
            style={{ height: 800 }}
            urls={{
              log: loggingSource,
            }}
            dateRange={logRange}
          />
        ),
      },
    ],
    [
      dateRange,
      grafanaSource,
      loggingSource,
      eventTableData,
      loading,
      logRange,
      onPageNoChange,
      reload,
    ]
  );

  const currentTabCmp = useMemo(
    () => contentList.find(({ name }) => name === currTab)?.component || null,
    [contentList, currTab]
  );

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
    sequencePromise([
      () => requestList({ loading: true, id: jobId }),
      initialData,
    ]);
    requestEvent({ ...defaultFilters, id: jobId });
    setCurrTab(contentList[0].name);
  }, []);

  useEffect(() => {
    setContextProps({
      handleStartClicked,
      handleStopClicked,
      handleEditClicked,
      handleCopyClicked,
      handleDeleteClicked,
      detail: detailData,
    });
  }, [detailData]);

  return (
    <div className="jobs-detail">
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
                title={(() =>
                  detailData?.hooks?.map((v) => v?.storage?.name || '-'))()}
              >
                存储挂载：
                <Tooltip
                  title={join(
                    detailData?.hooks,
                    '\n',
                    (v) =>
                      `挂载盘：${v?.storage?.name}\n路径：${v?.path}` || '-'
                  )}
                >
                  {join(detailData?.hooks, ',', (v) => v?.storage?.name || '-')}
                </Tooltip>
              </Col>
              <Col span={6} title={detailData?.mode}>
                任务模式：{detailData?.mode}
              </Col>
              <Col span={6} title={detailData?.startMode?.name}>
                启动方式：{detailData?.startMode?.name}
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
              <Col span={6} title={detailData?.workDir}>
                工作路径：{detailData?.workDir}
              </Col>
              <Col span={6} title={detailData?.source}>
                资源规格：{detailData?.source}
              </Col>
              <Col span={6} title={detailData?.nodes}>
                节点数量：{detailData?.nodes}
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
            {
              key: 'log',
              tab: '日志',
            },
          ]}
          onTabChange={onTabChange}
        >
          {currentTabCmp}
        </Card>
      </div>
    </div>
  );
};

JobDetail.context = (props = {}) => {
  const {
    handleStartClicked,
    handleStopClicked,
    handleEditClicked,
    handleCopyClicked,
    handleDeleteClicked,
    detail,
  } = props;
  const statusDesc = get(detail, 'status.desc');
  const _sname = get(detail, 'status.name');
  const statusName = getStatusName(_sname);
  const taskModel = get(detail, 'mode');

  const StartStopBtn = (props = {}) => {
    if (
      statusName === 'stopped' ||
      _sname === 'run_fail' ||
      _sname === 'start_fail'
    ) {
      return (
        <AuthButton
          required="jobs.list.edit"
          onClick={() => {
            handleStartClicked(detail);
          }}
          condition={[
            (user) => get(detail, 'creator.username') === get(user, 'username'),
          ]}
          {...props}
        >
          启动
        </AuthButton>
      );
    }
    if (statusName !== 'stopped') {
      return (
        <AuthButton
          required="jobs.list.edit"
          onClick={() => {
            handleStopClicked(detail);
          }}
          condition={[
            () => ['stop_fail', 'stop', 'completed'].indexOf(statusName) < 0,
            (user) => get(detail, 'creator.username') === get(user, 'username'),
          ]}
          {...props}
        >
          停止
        </AuthButton>
      );
    }
  };

  const DebugBtn = (props = {}) => (
    <AuthButton
      required="jobs.list"
      type="text"
      {...props}
      onClick={() => {
        const { url } = detail;
        window.open(url);
      }}
      condition={[
        () => ['running'].indexOf(statusName) > -1,
        (user) => get(detail, 'creator.username') === get(user, 'username'),
      ]}
    >
      调试
    </AuthButton>
  );

  const CopyBtn = (props = {}) => (
    <AuthButton
      required="jobs.list.edit"
      type="text"
      {...props}
      onClick={() => {
        handleCopyClicked(detail);
      }}
      condition={[
        () => ['error', 'stopped', 'completed'].indexOf(statusName) > -1,
        () => ['stop_fail'].indexOf(_sname) < 0,
        (user) => get(detail, 'creator.username') === get(user, 'username'),
      ]}
    >
      复制
    </AuthButton>
  );

  const EditBtn = (props = {}) => (
    <AuthButton
      required="jobs.list.edit"
      type="text"
      {...props}
      onClick={() => {
        handleEditClicked(detail);
      }}
      condition={[
        () => ['error', 'stopped', 'completed'].indexOf(statusName) > -1,
        () => ['stop_fail'].indexOf(_sname) < 0,
        (user) => get(detail, 'creator.username') === get(user, 'username'),
      ]}
    >
      编辑
    </AuthButton>
  );

  const DeleteBtn = () => (
    <AuthButton
      required="jobs.list.edit"
      type="text"
      onClick={() => {
        handleDeleteClicked(detail);
      }}
      condition={[
        () => ['stopped', 'error', 'completed'].indexOf(statusName) > -1,
        () => ['stop_fail'].indexOf(_sname) < 0,
        (user) => get(detail, 'creator.username') === get(user, 'username'),
      ]}
    >
      删除
    </AuthButton>
  );
  let items = [
    {
      key: 'copy',
      label: <CopyBtn />,
    },
    {
      key: 'delete',
      label: <DeleteBtn />,
    },
  ];

  if (taskModel === DEBUG) {
    items.unshift({
      key: 'edit',
      label: <EditBtn />,
    });
  }
  const menuProps = {
    items,
  };
  return (
    <Auth required="jobs.list.edit">
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
          {taskModel === DEBUG ? (
            <DebugBtn type="text" />
          ) : (
            <EditBtn type="text" />
          )}
        </Dropdown.Button>
        <StartStopBtn type="primary" />
      </Space>
    </Auth>
  );
};

JobDetail.path = '/jobs/list/detail';

export default JobDetail;
