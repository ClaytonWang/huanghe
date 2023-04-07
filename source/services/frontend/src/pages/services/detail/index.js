import { useCallback, useEffect, useMemo, useState } from 'react';
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
  Typography,
} from 'antd';
import { get } from 'lodash';
import moment from 'moment';
import ECharts from 'echarts-for-react';
import Icon from '@ant-design/icons';
import api from '@/common/api';
import { EventList, AuthButton } from '@/common/components';
import { transformDate } from '@/common/utils/helper';
import { ACTION, ADDRESS_TYPE, START, STOP, UPDATE } from '@/common/constants';
import Icons from '@/common/components/Icon';
import { useContextProps } from '@/common/hooks/RoutesProvider';
import LogList from './LogList';
import './index.less';

const { RangePicker } = DatePicker;

const ServiceDetail = () => {
  const { id: serviceId } = useParams();
  const [detailData, setDetailData] = useState({});
  const [monitorDataSource, setMonitorDataSource] = useState([]);
  const [eventTableData, setEventTableData] = useState({});
  const [logTableData, setLogTableData] = useState({});
  const [currTab, setCurrTab] = useState(null);
  const [dateRange, setDateRange] = useState({
    from: moment().add(-1, 'h'), // 默认1小时
    to: moment(),
  });
  const [loading, setLoading] = useState(false);
  const [eventLoading, setEventLoading] = useState(false);
  const setContextProps = useContextProps();
  const navigate = useNavigate();
  // TODO：日志事件范围
  // const [logRange, setLogRange] = useState({
  //   from: moment().add(-1, 'h'), // 默认1小时
  //   to: moment(),
  // });
  const { urls = [] } = detailData;
  const defaultFilters = {
    pageno: 1,
    pagesize: 5,
  };

  // eslint-disable-next-line react-hooks/exhaustive-deps
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

  const requestService = async (params) => {
    try {
      // setLoading(loading);
      const { result } = await api.servicesDetail(params);
      setDetailData(result);
      // setLoading(false);
    } catch (error) {
      console.log(error);
      // setLoading(false);
    }
  };

  const requestMonitorList = async (params) => {
    try {
      const { result } = await api.servicesDetailMonitor(params);
      setMonitorDataSource(result);
    } catch (error) {
      console.log(error);
    }
  };

  const requestEvent = async (args) => {
    const { pageno, pagesize, ...rest } = args;
    const params = { pageno, pagesize, ...rest };
    try {
      setEventLoading(true);
      const { result } = await api.servicesDetailEvent(params);
      setEventTableData({
        ...result,
        pageno,
        pagesize,
      });
    } catch (error) {
      console.log(error);
    } finally {
      setEventLoading(false);
    }
  };

  const requestLog = useCallback(
    async (args) => {
      const defaultFilters = {
        pageno: 1,
        pagesize: 10,
      };
      const params = {
        ...defaultFilters,
        ...args,
      };
      try {
        const { pageno, pagesize } = params;
        const { result } = await api.servicesDetailLog(params);
        const { data: _data = [] } = logTableData;
        const data = _data?.concat(result.data);
        setLogTableData({
          pageno,
          pagesize,
          total: result.total,
          data: [...data],
        });
      } catch (error) {
        console.log(error);
      }
    },
    [logTableData]
  );

  const reload = useCallback((args) => {
    requestService(args);
  }, []);

  const loadLog = useCallback(
    (args = {}) => {
      requestLog({
        id: serviceId,
        ...args,
      });
    },
    [requestLog, serviceId]
  );
  // TODO：Tab切换时日志列表刷新，原日志清空
  // const reloadLog = () => {
  //   setLogTableData({});
  //   loadLog();
  // };

  const handleStartClicked = async (record) => {
    try {
      const { id } = record;
      await api.servicesListAction({ id, action: ACTION[START] });
      message.success('已触发启动！');
    } catch (error) {
      console.log(error);
    }
  };
  const onStop = async (record) => {
    try {
      const { id } = record;
      await api.servicesListAction({ id, action: ACTION[STOP] });
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
    navigate('/services/list/update', {
      state: {
        params: values,
        type: UPDATE,
      },
    });
  };

  const deleteService = async (record) => {
    const { id } = record;
    try {
      await api.servicesListDelete({ id });
      message.success('删除Service成功！');
      navigate('/services/list');
    } catch (error) {
      console.log(error);
    }
  };

  const handleDelete = (record) => {
    Modal.confirm({
      title: '确定要删除该Service吗？',
      okText: '删除',
      okType: 'danger',
      cancelText: '取消',
      onOk: () => {
        deleteService(record);
      },
    });
  };

  const handleEventPageNoChange = useCallback(
    (pageno, pagesize) => {
      requestEvent({ id: serviceId, pageno, pagesize, action: 'event' });
    },
    [serviceId]
  );

  const onTabChange = (key) => {
    setCurrTab(key);
    // eslint-disable-next-line default-case
    switch (key) {
      case 'event':
        // requestEvent({ loading: true });
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

  const operations = useMemo(() => {
    if (currTab === 'event') return null;

    const from = moment(dateRange.from);
    const to = moment(dateRange.to);
    const dateFormat = 'YYYY/MM/DD HH:mm:ss';
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
  }, [currTab, dateRange.from, dateRange.to, rangePresets]);

  const Chart = ({ datasource = [[], []], name, unit }) => {
    const xData = datasource[0];
    const yData = datasource[1];
    const option = {
      title: {
        text: name,
      },
      tooltip: {
        show: true,
      },
      xAxis: {
        type: 'category',
        data: xData,
        axisLabel: {
          formatter: function (value) {
            return transformDate(value, 'YYYY-MM-DD HH:mm:ss');
          },
        },
      },
      yAxis: {
        type: 'value',
        name: unit,
      },
      series: [
        {
          data: yData,
          type: 'line',
          markPoint: {
            data: [
              {
                name: '最大值',
                type: 'max',
                symbolOffset: [0, -10],
                symbol: 'triangle',
                label: {
                  position: 'top',
                },
              },
              {
                name: '最小值',
                type: 'min',
                symbolOffset: [0, 10],
                symbol: 'triangle',
                label: {
                  position: 'bottom',
                },
              },
            ],
            symbolSize: 10,
          },
        },
      ],
    };
    return <ECharts option={option} />;
  };

  const ServicesMonitor = useMemo(
    () => (
      <div className="services-monitor">
        <Row gutter={[16, 24]}>
          {monitorDataSource.map(({ data, ...rest }, index) => (
            <Col key={index} span={8} title={rest.name}>
              <Chart key={index} datasource={data} {...rest} />
            </Col>
          ))}
        </Row>
      </div>
    ),
    [monitorDataSource]
  );

  const contentList = useMemo(
    () => [
      {
        name: 'chart',
        component: <ServicesMonitor />,
      },
      {
        name: 'event',
        component: (
          <EventList
            onPageNoChange={handleEventPageNoChange}
            tableData={eventTableData}
            reload={reload}
            loading={eventLoading}
          />
        ),
      },
      {
        name: 'log',
        component: (
          <LogList
            datasource={logTableData.data}
            total={logTableData.total}
            pageno={logTableData.pageno}
            pagesize={logTableData.pagesize}
            onLoadNext={loadLog}
          />
        ),
      },
    ],
    [
      ServicesMonitor,
      eventLoading,
      eventTableData,
      handleEventPageNoChange,
      loadLog,
      logTableData.data,
      logTableData.pageno,
      logTableData.pagesize,
      logTableData.total,
      reload,
    ]
  );

  const currentTabCmp = useMemo(
    () => contentList.find(({ name }) => name === currTab)?.component || null,
    [contentList, currTab]
  );

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    const timer = setInterval(() => {
      reload();
    }, 3000);
    return () => {
      clearInterval(timer);
    };
  }, []);

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestService({ id: serviceId });
    requestMonitorList({ id: serviceId });
    requestEvent({ ...defaultFilters, id: serviceId, action: 'event' });
    loadLog();
    setCurrTab(contentList[0].name);
  }, []);

  useEffect(() => {
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
              <Col span={6} title="公网访问">
                公网访问：{detailData?.isPublic ? '是' : '否'}
              </Col>
              <Col span={6} title="URL">
                URL：
                <span>
                  {urls.map(({ type, address }, index) => (
                    <Tooltip key={index} title={ADDRESS_TYPE[type]}>
                      <Typography.Paragraph
                        style={{ display: 'inline-block' }}
                        copyable={{ tooltips: false }}
                      >
                        {address}
                      </Typography.Paragraph>
                    </Tooltip>
                  ))}
                </span>
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

ServiceDetail.context = (props = {}) => {
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
            required="deployments.list.edit"
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
            required="deployments.list.edit"
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
            required="deployments.list.edit"
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
            required="deployments.list.edit"
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
        required="deployments.list"
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

ServiceDetail.path = '/services/list/detail/:id';

export default ServiceDetail;
