/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-01 15:53:49
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-02-24 11:03:07
 * @FilePath: /huanghe/source/services/frontend/src/pages/jobs/detail/index.js
 * @Description: detail page
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
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
  Button,
} from 'antd';
import Icon, { InfoCircleOutlined } from '@ant-design/icons';
import {
  ChartMonitor,
  EventMonitor,
  AuthButton,
  Auth,
} from '@/common/components';
import { get } from 'lodash';

import {
  purifyDeep,
  transformDate,
  getStatusName,
} from '@/common/utils/helper';
import api from '@/common/api';
import qs from 'qs';
import { JOB_ACTION, START, STOP, UPDATE, DEBUG, COPY } from '@/common/constants';
import Icons from '@/common/components/Icon';
import { useContextProps } from '@/common/hooks/RoutesProvider';
import moment from 'moment';

import './index.less';

const { RangePicker } = DatePicker;

const JobDetail = () => {
  const [tableData, setTableData] = useState([]);
  const [detailData, setDetailData] = useState(null);
  const [currTab, setCurrTab] = useState('chart');
  const [dateRange, setDateRange] = useState({
    from: moment().add(-1, 'h'), // 默认1小时
    to: moment(),
  });
  const [logRange, setLogRange] = useState({
    from: moment().add(-1, 'h'), // 默认1小时
    to: moment(),
  });
  const [loading, setLoading] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();
  const setContextProps = useContextProps();
  const navigate = useNavigate();

  const rangePresets = [
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
  ];

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
        const { result } = await api.jobDetail(params);
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
        const { result } = await api.jobDetailEvent(params);
        setTableData(result);
        setLoading(false);
      } catch (error) {
        console.log(error);
        setLoading(false);
      }
    },
    [getFilters]
  );

  const reload = useCallback(
    (args) => {
      const filters = getFilters();
      const params = purifyDeep({ ...filters, ...args });
      // 手动同步Url
      setSearchParams(qs.stringify(params));
      requestList(params);
    },
    [getFilters, requestList, setSearchParams]
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
    navigate('/jobs/list/update', {
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
    requestList({ loading: true });
    const filters = getFilters();
    setSearchParams(qs.stringify(filters));
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

  const onPageNoChange = (pageno, pagesize) => {
    const filters = getFilters();
    const params = purifyDeep({ ...filters, pageno, pagesize });
    // 手动同步Url
    setSearchParams(qs.stringify(params));
    requestEvent(params);
  };

  const onTabChange = (key) => {
    setCurrTab(key);
    // eslint-disable-next-line default-case
    switch (key) {
      case 'event':
        requestEvent({ loading: true });
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

  const onLogRangeChange = (dates) => {
    if (dates) {
      setLogRange({ from: dates[0]?.valueOf(), to: dates[1]?.valueOf() });
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
          presets={rangePresets}
          showTime
          format={dateFormat}
          onChange={onRangeChange}
          placement="bottomRight"
          defaultValue={[moment(from, dateFormat), moment(to, dateFormat)]}
        />
      );
    }

    if (currTab === 'log') {
      return (
        // <RangePicker
        //   allowClear={false}
        //   presets={rangePresets}
        //   showTime
        //   format={dateFormat}
        //   onChange={onLogRangeChange}
        //   placement="bottomRight"
        //   defaultValue={[
        //     moment(logRange.from, dateFormat),
        //     moment(logRange.to, dateFormat),
        //   ]}
        // />
        null
      );
    }
    return null;
  }, [currTab]);

  const contentList = {
    chart: <ChartMonitor urls={detailData?.grafana} dateRange={dateRange} />,
    event: (
      <EventMonitor
        onPageNoChange={onPageNoChange}
        tableData={tableData}
        reload={reload}
        loading={loading}
      />
    ),
    log: (
      <ChartMonitor
        style={{ height: 800 }}
        urls={{
          log: detailData?.loggingUrl,
        }}
        dateRange={logRange}
      />
    ),
  };

  return (
    <div className="detail">
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
                  title={(() =>
                    detailData?.hooks?.map((v) => v?.storage?.name || '-'))()}
                >
                  {(() =>
                    detailData?.hooks?.map((v) => v?.storage?.name || '-'))()}
                </Tooltip>
              </Col>
              <Col span={6} title={detailData?.image?.name}>
                镜像：
                <Tooltip title={detailData?.image?.name}>
                  {detailData?.image?.name}
                </Tooltip>
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
          {contentList[currTab]}
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
        <Dropdown.Button menu={menuProps}>
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
