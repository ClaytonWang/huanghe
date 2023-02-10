/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-01 15:53:49
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-10 15:01:29
 * @FilePath: /huanghe/source/services/frontend/src/pages/jobs/detail/index.js
 * @Description: detail page
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
  Col,
  Row,
  Tabs,
  Space,
  Skeleton,
  Dropdown,
  Tooltip,
  Spin,
  message,
  Modal,
  DatePicker,
} from 'antd';
import { useAuth } from '@/common/hooks/useAuth';
import Icon from '@ant-design/icons';
import { ChartMonitor, EventMonitor, AuthButton } from '@/common/components';
import { get } from 'lodash';

import { purifyDeep, transformDate } from '@/common/utils/helper';
import api from '@/common/api';
import qs from 'qs';
import { USER, JOB_ACTION, START, STOP, UPDATE } from '@/common/constants';
import Icons from '@/common/components/Icon';
import { useContextProps } from '@/common/hooks/RoutesProvider';
import moment from 'moment';

import './index.less';

const { RangePicker } = DatePicker;

const JobDetail = () => {
  const [tableData, setTableData] = useState([]);
  const [detailData, setDetailData] = useState(null);
  const [currTab, setCurrTab] = useState('');
  const [dateRange, setDateRange] = useState({
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
  const handleStopClicked = async (record) => {
    try {
      const { id } = record;
      await api.jobListAction({ id, action: JOB_ACTION[STOP] });
      message.success('已触发停止！');
    } catch (error) {
      console.log(error);
    }
  };
  const handleEditClicked = (values) => {
    navigate('/jobs/list/update', {
      state: {
        params: values,
        type: UPDATE,
      },
    });
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

  const handleDelete = (record) => {
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
      handleDelete,
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
      case 'event-monitor':
        requestEvent({ loading: true });
        break;
    }
  };

  const onRangeChange = (dates) => {
    if (dates) {
      console.log('From: ', dates[0], ', to: ', dates[1]);
      setDateRange({ from: dates[0]?.valueOf(), to: dates[1]?.valueOf() });
    } else {
      console.log('Clear');
    }
  };

  const operations = useMemo(() => {
    if (currTab === 'event-monitor') return null;

    const dateFormat = 'YYYY/MM/DD HH:mm:ss';
    return (
      <RangePicker
        allowClear={false}
        presets={rangePresets}
        showTime
        format={dateFormat}
        onChange={onRangeChange}
        placement="bottomRight"
        defaultValue={[
          moment(dateRange.from, dateFormat),
          moment(dateRange.to, dateFormat),
        ]}
      />
    );
  }, [currTab]);

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
                {(() =>
                  detailData?.hooks?.map((v) => v?.storage?.name || '-'))()}
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
            </>
          )}
        </Row>
      </div>
      <div className="dbr-table-container">
        <Tabs
          defaultActiveKey="chart-monitor"
          tabBarExtraContent={operations}
          items={[
            {
              key: 'chart-monitor',
              label: `监控`,
              children: (
                <ChartMonitor
                  urls={detailData?.grafana}
                  dateRange={dateRange}
                />
              ),
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
          onChange={onTabChange}
        />
      </div>
    </div>
  );
};

JobDetail.context = (props = {}) => {
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
            required="jobs.list.edit"
            type="link"
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
            required="jobs.list.edit"
            type="link"
            onClick={() => {
              handleDelete(detail);
            }}
            condition={[
              () => ['stopped', 'error'].indexOf(statusName) > -1,
              (user) => {
                if (user.role.name === USER) {
                  return (
                    get(detail, 'creator.username') === get(user, 'username')
                  );
                }
                return true;
              },
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
        {statusName === 'stopped' && (
          <AuthButton
            required="jobs.list.edit"
            type="text"
            onClick={() => {
              handleStartClicked(detail);
            }}
            condition={[
              (user) => {
                if (user.role.name === USER) {
                  return (
                    get(detail, 'creator.username') === get(user, 'username')
                  );
                }
                return true;
              },
            ]}
          >
            启动
          </AuthButton>
        )}
        {statusName !== 'stopped' && (
          <AuthButton
            required="jobs.list.edit"
            type="text"
            style={(() => {
              if (statusName === 'error') {
                return { color: '#00000040' };
              }
            })()}
            onClick={() => {
              const { user } = useAuth();
              if (get(detail, 'creator.username') === get(user, 'username')) {
                handleStopClicked(detail);
              }
            }}
            condition={[
              () => ['error', 'stop'].indexOf(statusName) < 0,
              (user) => {
                if (user.role.name === USER) {
                  return (
                    get(detail, 'creator.username') === get(user, 'username')
                  );
                }
                return true;
              },
            ]}
          >
            停止
          </AuthButton>
        )}
      </Dropdown.Button>
      <AuthButton
        required="jobs.list"
        type="primary"
        onClick={() => {
          const { url } = detail;
          window.open(url);
        }}
        condition={[
          () => ['running'].indexOf(statusName) > -1,
          (user) => {
            if (user.role.name === USER) {
              return get(detail, 'creator.username') === get(user, 'username');
            }
            return true;
          },
        ]}
      >
        打开
      </AuthButton>
    </Space>
  );
};

JobDetail.path = '/jobs/list/detail';

export default JobDetail;
